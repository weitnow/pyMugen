import pygame
from gamestates.gamestate_base import GameState
from gameobjects.fighter import Fighter, GameObject

class PlayingState(GameState):

    def enter(self):
           # --- Create objects ---
        player = Fighter((100, 100), 0) # 0 = player index = player 1 TODO: refactor this
        player.get_anim("gbFighter")
        player.get_anim("nesFighter")
        player.set_anim("nesFighter")
        player.set_frame_tag("Idle")

        player.set_hurtbox(pygame.Rect(0, 0, 24, 32))
        player.set_hitbox(pygame.Rect(27, 10, 5, 5))

        self.player = player

        # stage
        stage = GameObject((0, 0))
        stage.get_anim("stages")
        stage.set_anim("stages")
        stage.set_frame_tag("Level")

        self.stage = stage

    def exit(self):
        pass

    def update(self, dt):
        self.player.controller.update()
        self.player.update(dt)
        self.stage.update(dt)

        # --- Input Handling ---
        # Player 1
        #pressed_p1 = input_manager.get_pressed_actions(0)
        #just_pressed_p1 = input_manager.get_just_pressed_actions(0)

        # Player 2
        #pressed_p2 = input_manager.get_pressed_actions(1)
        #just_pressed_p2 = input_manager.get_just_pressed_actions(1)

    def draw(self):
        self.stage.draw(self.view_manager.game_surface)
        self.player.draw(self.view_manager.game_surface)

    def debug_draw(self): #optional
        self.player.draw_debug(self.view_manager.debug_surface, self.view_manager.to_debug_coords)