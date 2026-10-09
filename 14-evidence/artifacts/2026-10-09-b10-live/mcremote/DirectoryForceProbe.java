import java.nio.channels.FileChannel;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

/** CredentialStore.forceDirectory と同じ操作を既存 directory にだけ行う診断。 */
public class DirectoryForceProbe {
    public static void main(String[] args) {
        System.out.println("os=" + System.getProperty("os.name"));
        System.out.println("java=" + Runtime.version());
        if (args.length != 1) {
            System.out.println("usage: java DirectoryForceProbe.java <existing-directory>");
            System.exit(2);
        }
        String stage = "validate-directory";
        try {
            Path directory = Path.of(args[0]).toAbsolutePath().normalize();
            if (!Files.isDirectory(directory, LinkOption.NOFOLLOW_LINKS)) {
                throw new IllegalArgumentException("Target is not an existing non-symlink directory");
            }
            stage = "open-directory-read";
            try (FileChannel channel = FileChannel.open(directory, StandardOpenOption.READ)) {
                stage = "force-directory";
                channel.force(true);
                stage = "close-channel";
            }
            System.out.println("result=OK");
        } catch (Exception failure) {
            System.out.println("result=ERROR");
            System.out.println("stage=" + stage);
            System.out.println("exception=" + failure.getClass().getName());
            // exception message は private path を含み得るので出さない。
            for (StackTraceElement frame : failure.getStackTrace()) {
                System.out.println("at=" + frame.getClassName() + "." + frame.getMethodName()
                        + ":" + frame.getLineNumber());
            }
            System.exit(1);
        }
    }
}
