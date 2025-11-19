import pygame
from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject
from gameobjects.fighter import Fighter
from input_manager import PlayerController, Action
from resource_manager import ResourceManager
from sprite import Sprite  # your Sprite class


# -----------------------
# PlayingState
# -----------------------
class PlayingState(GameState):

    def enter(self):
        # --- Create Fighter ---
        player = Fighter((100, 100), player_index=0)

        # Create Sprite for the fighter
        sprite = Sprite(rotatable=True)
        # load the animation
        sprite.get_anim("gbFighter")
        sprite.set_anim("gbFighter")
        sprite.set_frame_tag("Walk")

        # Attach sprite to the player GameObject
        player.add_sprite(sprite)

        # Setup hitbox / hurtbox
        player.set_hurtbox(pygame.Rect(0, 0, 24, 32))
        player.set_hitbox(pygame.Rect(27, 10, 5, 5))

        self.player = player

    def exit(self):
        pass

    def update(self, dt):
        self.player.controller.update()
        self.player.update(dt)

    def draw(self):
        self.player.draw(self.view_manager.game_surface)

    def debug_draw(self):
        self.player.draw_debug(self.view_manager.debug_surface)