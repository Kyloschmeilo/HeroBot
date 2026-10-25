package hero.bane.herobot.paper.util;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.component.SwingAnimation;

/**
 * Arm swings for bots. Since 26.3 a swing carries a {@link SwingAnimation}; vanilla picks the
 * held item's attack animation for punches and mining, and its interact animation for item use.
 * Bots have no client predicting the swing, so it is always sent to the swinging player as well.
 */
public final class Swings {
    private Swings() {
    }

    /** Punch, attack or mining swing, like a vanilla left click. */
    public static void attack(LivingEntity entity, InteractionHand hand) {
        entity.swing(hand, entity.getItemInHand(hand).getAttackAnimation(), true);
    }

    public static void attack(LivingEntity entity) {
        attack(entity, InteractionHand.MAIN_HAND);
    }

    /** Swing after using an item or a block, like a vanilla right click. */
    public static void interact(LivingEntity entity, InteractionHand hand) {
        entity.swing(hand, entity.getItemInHand(hand).getInteractAnimation(), true);
    }

    /** Swing that does not depend on the held item, e.g. after dropping it. */
    public static void plain(LivingEntity entity, InteractionHand hand) {
        entity.swing(hand, SwingAnimation.DEFAULT, true);
    }
}
