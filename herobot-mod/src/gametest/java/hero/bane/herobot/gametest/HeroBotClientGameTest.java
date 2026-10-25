package hero.bane.herobot.gametest;

import hero.bane.herobot.common.ai.Comment;
import hero.bane.herobot.mod.client.HeroBotClient;
import hero.bane.herobot.mod.client.screen.ai.AiEditorScreen;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import org.lwjgl.sdl.SDLScancode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.spongepowered.asm.mixin.MixinEnvironment;

import java.util.ArrayList;
import java.util.List;

/**
 * Starts the real client with HeroBot and checks the parts a dedicated server cannot reach:
 * every mixin applying, bots showing up client side, the server remote-controlling the local
 * player through simulated input, and the HeroScript editor screen.
 * Each step logs "SMOKE OK name" or "SMOKE FAIL name" and the test fails at the end if any failed.
 */
public class HeroBotClientGameTest implements FabricClientGameTest {
    private static final Logger LOGGER = LoggerFactory.getLogger("HeroBotClientGameTest");

    private final List<String> failures = new ArrayList<>();

    private void step(String name, Runnable body) {
        try {
            body.run();
            LOGGER.info("SMOKE OK client_{}", name);
        } catch (Throwable t) {
            failures.add(name);
            LOGGER.error("SMOKE FAIL client_{}: {}", name, t.toString(), t);
        }
    }

    @Override
    public void runTest(ClientGameTestContext context) {
        LOGGER.info("SMOKE START client");
        try (TestSingleplayerContext singleplayer = context.worldBuilder().create()) {
            singleplayer.getConnection().waitForChunksRender();

            // Applies every mixin of every mod now instead of on first use.
            step("mixin_audit", () -> MixinEnvironment.getCurrentEnvironment().audit());

            String self = context.computeOnClient(client -> client.player.getName().getString());
            BlockPos pos = context.computeOnClient(client -> client.player.blockPosition());

            step("bot_visible", () -> {
                singleplayer.getServer().runCommand("playerspawn TestBot at %d %d %d facing north in survival"
                        .formatted(pos.getX() + 3, pos.getY(), pos.getZ()));
                context.waitFor(client -> client.level != null && client.level.players().stream()
                        .anyMatch(p -> p.getName().getString().equals("TestBot")), 600);
                context.waitTicks(20);
                context.takeScreenshot("herobot-bot-visible");
            });

            step("bot_actions", () -> {
                singleplayer.getServer().runCommand("player TestBot look upon " + self);
                singleplayer.getServer().runCommand("player TestBot swing once");
                singleplayer.getServer().runCommand("player TestBot jump continuous");
                singleplayer.getServer().runCommand("player TestBot sneak");
                context.waitTicks(40);
                singleplayer.getServer().runCommand("player TestBot stop");
            });

            step("remote_jump", () -> {
                double startY = context.computeOnClient(client -> client.player.getY());
                singleplayer.getServer().runCommand("player " + self + " jump once");
                context.waitFor(client -> client.player.getY() > startY + 0.3, 60);
            });

            step("remote_drop_key", () -> {
                singleplayer.getServer().runCommand("give " + self + " minecraft:stone 3");
                context.waitFor(client -> client.player.getInventory().getSelectedItem().getCount() == 3, 60);
                singleplayer.getServer().runCommand("player " + self + " drop once");
                context.waitFor(client -> client.player.getInventory().getSelectedItem().getCount() == 2, 60);
            });

            step("remote_swing", () -> {
                singleplayer.getServer().runCommand("player " + self + " swing once");
                context.waitTicks(10);
            });

            step("editor_opens", () -> {
                context.getInput().pressKey(HeroBotClient.openAiEditorKey);
                context.waitForScreen(AiEditorScreen.class);
                context.waitTicks(20);
                context.takeScreenshot("herobot-editor");
            });

            step("editor_comment_typing", () -> {
                context.runOnClient(client -> ((AiEditorScreen) client.gui.screen()).addComment(0, 0, -1));
                context.waitTick();
                context.getInput().typeChars("hello bot");
                context.waitTick();
                context.takeScreenshot("herobot-editor-comment");
                context.getInput().pressKey(SDLScancode.SDL_SCANCODE_ESCAPE);
                context.waitTick();
                String text = context.computeOnClient(client -> {
                    List<Comment> comments = ((AiEditorScreen) client.gui.screen()).script().comments();
                    return comments.isEmpty() ? "<none>" : comments.getLast().text();
                });
                if (!text.equals("hello bot")) throw new AssertionError("comment text was '" + text + "'");
            });

            step("editor_shortcuts_and_close", () -> {
                context.getInput().holdControl();
                context.getInput().pressKey(SDLScancode.SDL_SCANCODE_Z);
                context.getInput().releaseControl();
                context.waitTick();
                context.getInput().pressKey(SDLScancode.SDL_SCANCODE_ESCAPE);
                context.waitForScreen(null);
            });

            step("bot_disconnect", () -> {
                singleplayer.getServer().runCommand("player TestBot disconnect");
                context.waitFor(client -> client.level.players().stream()
                        .noneMatch(p -> p.getName().getString().equals("TestBot")), 100);
            });
        }
        LOGGER.info("SMOKE DONE client");
        if (!failures.isEmpty()) throw new AssertionError("failed client checks: " + failures);
    }
}
