#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 5 ]; then
  echo "usage: $0 <sender-ssh-alias> <target-ssh-alias> <target-wake-alias> <python|wakeonlan> <deep|poweroff>" >&2
  exit 2
fi

sender_name="$1"
target_name="$2"
target_wake_alias="$3"
sender_method="$4"
power_state="$5"

case "$sender_method" in
  python|wakeonlan) ;;
  *)
    echo "unsupported sender method: $sender_method" >&2
    exit 2
    ;;
esac

case "$power_state" in
  deep|poweroff) ;;
  *)
    echo "unsupported power state: $power_state" >&2
    exit 2
    ;;
esac

ssh_options=(
  -o BatchMode=yes
  -o ConnectTimeout=3
  -o ConnectionAttempts=1
  -o ControlMaster=no
  -o ControlPath=none
  -o ControlPersist=no
  -o ServerAliveInterval=2
  -o ServerAliveCountMax=1
)

resolve_private_mac() {
  local alias_name="$1"
  bash -ic "alias $alias_name" 2>/dev/null |
    sed -nE "s/^alias [^=]+='wakeonlan ([^' ]+)'.*/\\1/p"
}

target_mac="$(resolve_private_mac "$target_wake_alias")"
if [ -z "$target_mac" ]; then
  echo "private wake alias could not be resolved" >&2
  exit 1
fi

remote_health() {
  local host_name="$1"
  ssh "${ssh_options[@]}" "$host_name" '
    running_count=$(docker ps -q 2>/dev/null | wc -l)
    nonhealthy_count=$(
      docker ps --format "{{.Status}}" 2>/dev/null |
        awk "!/Up .*\\(healthy\\)/{n++} END{print n+0}"
    )
    printf "%s %s\n" "$running_count" "$nonhealthy_count"
  '
}

remote_default_cidr() {
  local host_name="$1"
  ssh "${ssh_options[@]}" "$host_name" '
    default_interface=$(
      ip -4 route show default |
        awk "NR == 1 {for (i = 1; i <= NF; i++) if (\$i == \"dev\") print \$(i + 1)}"
    )
    if [ -z "$default_interface" ]; then
      exit 1
    fi
    ip -4 -o addr show dev "$default_interface" scope global |
      awk "NR == 1 {print \$4}"
  '
}

cidr_broadcast() {
  local interface_cidr="$1"
  python3 -c '
import ipaddress
import sys

print(ipaddress.ip_interface(sys.argv[1]).network.broadcast_address)
' "$interface_cidr"
}

if ! ssh "${ssh_options[@]}" "$sender_name" true; then
  echo "sender is not reachable" >&2
  exit 1
fi
if ! ssh "${ssh_options[@]}" "$target_name" true; then
  echo "target is not reachable" >&2
  exit 1
fi

sender_cidr="$(remote_default_cidr "$sender_name")"
target_cidr="$(remote_default_cidr "$target_name")"
sender_broadcast="$(cidr_broadcast "$sender_cidr")"
target_broadcast="$(cidr_broadcast "$target_cidr")"
if [ "$sender_broadcast" != "$target_broadcast" ]; then
  echo "sender and target default LAN broadcast addresses do not match" >&2
  exit 1
fi

sender_default_interface="$(
  ssh "${ssh_options[@]}" "$sender_name" '
    ip -4 route show default |
      awk "NR == 1 {for (i = 1; i <= NF; i++) if (\$i == \"dev\") print \$(i + 1)}"
  '
)"
sender_broadcast_interface="$(
  ssh "${ssh_options[@]}" "$sender_name" ip -4 route get "$target_broadcast" |
    awk 'NR == 1 {for (i = 1; i <= NF; i++) if ($i == "dev") print $(i + 1)}'
)"
if [ -z "$sender_default_interface" ] ||
  [ "$sender_broadcast_interface" != "$sender_default_interface" ]; then
  echo "directed broadcast does not use the sender default LAN interface" >&2
  exit 1
fi

pre_boot_id="$(ssh "${ssh_options[@]}" "$target_name" cat /proc/sys/kernel/random/boot_id)"
read -r expected_running pre_nonhealthy < <(remote_health "$target_name")
if [ "$expected_running" -lt 1 ] || [ "$pre_nonhealthy" -ne 0 ]; then
  echo "target preflight health is not clean" >&2
  exit 1
fi

echo "READY sender=$sender_name target=$target_name method=$sender_method state=$power_state expected_containers=$expected_running"
echo "Waiting for three consecutive unreachable checks before sending a packet."

offline_deadline=$((SECONDS + 180))
consecutive_unreachable=0
while [ "$SECONDS" -lt "$offline_deadline" ]; do
  if ssh "${ssh_options[@]}" "$target_name" true >/dev/null 2>&1; then
    consecutive_unreachable=0
  else
    consecutive_unreachable=$((consecutive_unreachable + 1))
    echo "UNREACHABLE count=$consecutive_unreachable"
    if [ "$consecutive_unreachable" -ge 3 ]; then
      break
    fi
  fi
  sleep 2
done

if [ "$consecutive_unreachable" -lt 3 ]; then
  echo "FAIL target did not become unreachable within 180 seconds" >&2
  exit 1
fi

sleep 3
case "$power_state" in
  deep)
    if ssh "${ssh_options[@]}" "$target_name" true >/dev/null 2>&1; then
      echo "FAIL target recovered before the magic packet was sent" >&2
      exit 1
    fi
    ;;
  poweroff)
    echo "WAITING_POWER_OFF_CONFIRMATION"
    echo "Confirm physical power-off before allowing packet transmission."
    IFS= read -r poweroff_confirmation
    if [ "$poweroff_confirmation" != "POWER_OFF_CONFIRMED" ]; then
      echo "FAIL invalid power-off confirmation" >&2
      exit 1
    fi
    if ssh "${ssh_options[@]}" "$target_name" true >/dev/null 2>&1; then
      echo "FAIL target is reachable after power-off confirmation" >&2
      exit 1
    fi
    ;;
esac

if ! ssh "${ssh_options[@]}" "$sender_name" true; then
  echo "FAIL sender became unreachable" >&2
  exit 1
fi

sent_at="$(date +%s)"
case "$sender_method" in
  wakeonlan)
    ssh "${ssh_options[@]}" "$sender_name" wakeonlan -i "$target_broadcast" "$target_mac" |
      sed -E \
        -e 's/([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}/<redacted-mac>/g' \
        -e 's/([[:digit:]]{1,3}\.){3}[[:digit:]]{1,3}/<redacted-broadcast>/g'
    ;;
  python)
    python_sender='import socket
import sys
mac = bytes.fromhex(sys.argv[1].replace(":", ""))
packet = b"\xff" * 6 + mac * 16
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sent = sock.sendto(packet, (sys.argv[2], 9))
print(f"python packet bytes: {sent}")'
    printf '%s\n' "$python_sender" |
      ssh "${ssh_options[@]}" "$sender_name" python3 - "$target_mac" "$target_broadcast"
    ;;
esac

echo "PACKET_SENT method=$sender_method"

recovery_deadline=$((SECONDS + 180))
while [ "$SECONDS" -lt "$recovery_deadline" ]; do
  if ssh "${ssh_options[@]}" "$target_name" true >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

if ! ssh "${ssh_options[@]}" "$target_name" true >/dev/null 2>&1; then
  echo "FAIL target did not recover SSH within 180 seconds" >&2
  exit 1
fi

ssh_recovered_at="$(date +%s)"
post_boot_id="$(ssh "${ssh_options[@]}" "$target_name" cat /proc/sys/kernel/random/boot_id)"

case "$power_state" in
  deep)
    if [ "$post_boot_id" != "$pre_boot_id" ]; then
      echo "FAIL boot ID changed after deep sleep" >&2
      exit 1
    fi
    ;;
  poweroff)
    if [ "$post_boot_id" = "$pre_boot_id" ]; then
      echo "FAIL boot ID did not change after poweroff" >&2
      exit 1
    fi
    ;;
esac

health_deadline=$((SECONDS + 180))
while [ "$SECONDS" -lt "$health_deadline" ]; do
  read -r running_count nonhealthy_count < <(remote_health "$target_name")
  if [ "$running_count" -eq "$expected_running" ] && [ "$nonhealthy_count" -eq 0 ]; then
    break
  fi
  sleep 3
done

read -r running_count nonhealthy_count < <(remote_health "$target_name")
if [ "$running_count" -ne "$expected_running" ] || [ "$nonhealthy_count" -ne 0 ]; then
  echo "FAIL container health did not recover within 180 seconds" >&2
  exit 1
fi

health_recovered_at="$(date +%s)"
echo "PASS state=$power_state method=$sender_method ssh_seconds=$((ssh_recovered_at - sent_at)) health_seconds=$((health_recovered_at - sent_at)) containers=$running_count"
