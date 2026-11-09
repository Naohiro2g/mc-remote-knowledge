package gate;

import java.net.InetSocketAddress;
import java.lang.reflect.Method;
import org.bukkit.World;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.java.JavaPlugin;

public final class StackGateProbe extends JavaPlugin {
    @Override
    public void onEnable() {
        getServer().getScheduler().runTaskLater(this, this::check, 100L);
    }

    private void check() {
        try {
            int enabled = 0;
            for (Plugin plugin : getServer().getPluginManager().getPlugins()) {
                if (plugin.getName().equals("StackGateProbe")) continue;
                getLogger().info("PLUGIN " + plugin.getName() + " enabled=" + plugin.isEnabled());
                if (!plugin.isEnabled() && !plugin.getName().equals("DiscordSRV")) {
                    throw new IllegalStateException("Unexpected disabled plugin: " + plugin.getName());
                }
                if (plugin.isEnabled()) enabled++;
            }
            getLogger().info("PRODUCT_PLUGIN_CHECK enabled=" + enabled + " DiscordSRV_external_connection_not_tested=true");
            int dimensions = 0;
            for (World world : getServer().getWorlds()) {
                world.getChunkAt(0, 0);
                getLogger().info("DIMENSION " + world.getKey() + " chunk_0_0_read=true");
                dimensions++;
            }
            if (dimensions != 3) throw new IllegalStateException("Expected 3 dimensions, got " + dimensions);
            getServer().getScheduler().runTaskAsynchronously(this, this::checkPing);
        } catch (Throwable error) {
            getLogger().severe("STACK_GATE_PROBE_FAIL " + error);
        }
    }

    private void checkPing() {
        try {
            Plugin geyser = getServer().getPluginManager().getPlugin("Geyser-Spigot");
            Object ping = geyser.getClass().getMethod("getGeyserPingPassthrough").invoke(geyser);
            Method method = ping.getClass().getMethod("getPingInformation", InetSocketAddress.class);
            Object info = method.invoke(ping, new InetSocketAddress("127.0.0.1", 19132));
            if (info == null) throw new IllegalStateException("Geyser ping returned null");
            getLogger().info("GEYSER_PING_PASS implementation=" + ping.getClass().getSimpleName());
            getLogger().info("STACK_GATE_PROBE_PASS");
        } catch (Throwable error) {
            getLogger().severe("STACK_GATE_PROBE_FAIL " + error);
        }
    }
}
