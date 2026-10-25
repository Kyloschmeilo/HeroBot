package hero.bane.herobot.mod.client.mixin;

import com.llamalad7.mixinextras.sugar.Local;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.entity.EntityRenderDispatcher;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.vehicle.minecart.AbstractMinecart;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(EntityRenderDispatcher.class)
public abstract class EntityRenderDispatcherMixin {
    // shouldRender gained a partial tick argument in 26.3; only the entity is needed, so it is
    // captured by type and the rest of the signature can keep changing.
    @Inject(method = "shouldRender", at = @At("HEAD"), cancellable = true)
    private void herobot$hideTaggedMinecarts(CallbackInfoReturnable<Boolean> cir,
                                             @Local(argsOnly = true) Entity entity) {
        if (entity instanceof AbstractMinecart cart
                && (cart.isInvisible() || cart.entityTags().contains("invisible"))) {
            LocalPlayer viewer = Minecraft.getInstance().player;
            if (viewer == null || !viewer.isSpectator()) {
                cir.setReturnValue(false);
            }
        }
    }
}
