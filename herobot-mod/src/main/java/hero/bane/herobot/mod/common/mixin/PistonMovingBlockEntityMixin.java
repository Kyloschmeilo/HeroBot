package hero.bane.herobot.mod.common.mixin;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import hero.bane.herobot.mod.common.bot.BotPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.block.piston.PistonMovingBlockEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;

@Mixin(PistonMovingBlockEntity.class)
public class PistonMovingBlockEntityMixin {

    /**
     * Slime block pistons only launch entities whose movement this side simulates; for players
     * that is their client. Bots have no client, so the server launches them instead.
     * (Before 26.3 vanilla skipped every {@code ServerPlayer} here instead.)
     */
    @WrapOperation(
            method = "moveCollidedEntities",
            at = @At(value = "INVOKE", target = "Lnet/minecraft/world/entity/Entity;canSimulateMovement()Z")
    )
    private static boolean herobot$bounceBotPlayers(Entity entity, Operation<Boolean> original) {
        return entity instanceof BotPlayer || original.call(entity);
    }
}
