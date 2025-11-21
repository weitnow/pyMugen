import pygame
from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from resource_manager import ResourceManager
from sprite import Sprite  # your Sprite class


# -----------------------
# PlayingState
# -----------------------
class PlayingState(GameState):

    def enter(self):
        # --- Create Fighter ---
        player = GameObject((100, 100))

        # Create Sprite for the fighter
        sprite = Sprite()
        # load the animation
        sprite.load_anim("gbFighter")
        sprite.load_anim("nesFighter")
        sprite.set_anim("nesFighter")
        sprite.set_frame_tag("Idle")

        # Attach sprite to the player GameObject
        player.add_sprite(sprite)



        # Setup hitbox / hurtbox
        # Usage examples:

        # Example 1: Hitbox active for all frames of "player_attack" animation
        player.add_hitbox(
            pygame.Rect(20, 10, 30, 40), 
            HitboxType.HIGH, 
            base_name="gbFighter"
        )

        # Example 2: Hurtbox active only during "idle" tag of "player" animation
        player.add_hurtbox(
            pygame.Rect(0, 0, 32, 64),
            HurtboxType.PUNCH,
            base_name="gbFighter",
            tag_name="Idle"
        )

        # Example 3: Hitbox active only on frame 5 of "player_attack" animation
        player.add_hitbox(
            pygame.Rect(32, 0, 5, 5),
            HitboxType.LOW,
            base_name="nesFighter",
            frame=2
        )



        self.player = player

    def exit(self):
        pass

    def handle_input(self):
        pass

    def update(self, dt):
        self.player.update(dt)

        # Example 4: Query active boxes
        active_hitboxes = self.player.get_active_hitboxes()
        for rect, hitbox_type in active_hitboxes:
            print(f"Active hitbox: {hitbox_type} at {rect}")

        active_hurtboxes = self.player.get_active_hurtboxes()
        for rect, hurtbox_type in active_hurtboxes:
            print(f"Active hurtbox: {hurtbox_type} at {rect}")

    def draw(self):
        self.player.draw(self.view_manager.game_surface)

    def debug_draw(self):
        self.player.draw_debug(self.view_manager.debug_surface)