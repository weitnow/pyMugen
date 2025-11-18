import pygame
from gamestates.gamestate import GameState
from gameobjects.fighter import Fighter

class PlayingState(GameState):

    def enter(self):
           # --- Create objects ---
        player = Fighter((100, 100), 0) # 0 = player index = player 1 TODO: refactor this
        player.get_anim("gbFighter")
        player.get_anim("nesFighter")
        player.set_anim("nesFighter")
        player.set_frame_tag("Idle")

        player.set_hurtbox(pygame.Rect(5, 10, 20, 30))
        player.set_hitbox(pygame.Rect(25, 10, 20, 15))

        self.player = player

    def exit(self):
        pass


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.change_state("menu")

    def update(self, dt):
        self.player.controller.update()
        self.player.update(dt)

        # --- Input Handling ---
        # Player 1
        #pressed_p1 = input_manager.get_pressed_actions(0)
        #just_pressed_p1 = input_manager.get_just_pressed_actions(0)

        # Player 2
        #pressed_p2 = input_manager.get_pressed_actions(1)
        #just_pressed_p2 = input_manager.get_just_pressed_actions(1)

    def draw(self):
        self.player.draw(self.view.game_surface)

    def debug_draw(self): #optional
        self.player.draw_debug(self.view.debug_surface, self.view.to_debug_coords)