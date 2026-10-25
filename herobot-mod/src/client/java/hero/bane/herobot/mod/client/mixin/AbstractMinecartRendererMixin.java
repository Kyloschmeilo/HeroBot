package hero.bane.herobot.mod.client.mixin;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.Model;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.AbstractMinecartRenderer;
import net.minecraft.client.renderer.entity.state.MinecartRenderState;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.resources.Identifier;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;

/**
 * Draws invisible minecarts as translucent ghosts for spectators.
 * <p>
 * 26.3 removed the crumbling overlay argument from {@code submitModel}. Both the texture and the
 * render type overloads are wrapped and neither is required, so if the renderer's call changes
 * again the carts simply render as in vanilla instead of crashing the client.
 */
@SuppressWarnings({"rawtypes", "unchecked"})
@Mixin(AbstractMinecartRenderer.class)
public abstract class AbstractMinecartRendererMixin {
    @Unique
    private static final Identifier herobot$MINECART_LOCATION =
            Identifier.withDefaultNamespace("textures/entity/minecart.png");

    @Unique
    private static final int herobot$GHOST_COLOR = 654311423;

    @Unique
    private static boolean herobot$isGhost(Object state) {
        LocalPlayer viewer = Minecraft.getInstance().player;
        return state instanceof MinecartRenderState cart && cart.isInvisible && viewer != null && viewer.isSpectator();
    }

    @Unique
    private static void herobot$submitGhost(SubmitNodeCollector collector, Model model, Object state,
                                            PoseStack poseStack, int light, int overlay) {
        collector.submitModel(model, state, poseStack,
                RenderTypes.entityTranslucent(herobot$MINECART_LOCATION),
                light, overlay, herobot$GHOST_COLOR);
    }

    @WrapOperation(
            method = "submit",
            require = 0,
            at = @At(
                    value = "INVOKE",
                    target = "Lnet/minecraft/client/renderer/SubmitNodeCollector;submitModel(Lnet/minecraft/client/model/Model;Ljava/lang/Object;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/resources/Identifier;III)V"
            )
    )
    private void herobot$ghostInvisibleCartTexture(SubmitNodeCollector collector, Model model, Object state,
                                                   PoseStack poseStack, Identifier texture, int light, int overlay,
                                                   int color, Operation<Void> original) {
        if (herobot$isGhost(state)) {
            herobot$submitGhost(collector, model, state, poseStack, light, overlay);
        } else {
            original.call(collector, model, state, poseStack, texture, light, overlay, color);
        }
    }

    @WrapOperation(
            method = "submit",
            require = 0,
            at = @At(
                    value = "INVOKE",
                    target = "Lnet/minecraft/client/renderer/SubmitNodeCollector;submitModel(Lnet/minecraft/client/model/Model;Ljava/lang/Object;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/rendertype/RenderType;III)V"
            )
    )
    private void herobot$ghostInvisibleCartRenderType(SubmitNodeCollector collector, Model model, Object state,
                                                      PoseStack poseStack, RenderType renderType, int light,
                                                      int overlay, int color, Operation<Void> original) {
        if (herobot$isGhost(state)) {
            herobot$submitGhost(collector, model, state, poseStack, light, overlay);
        } else {
            original.call(collector, model, state, poseStack, renderType, light, overlay, color);
        }
    }
}
