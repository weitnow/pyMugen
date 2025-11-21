import pygame
from gamestates.gamestate_base import GameState
from input_manager import Action
from sprite import Sprite

class MenuState(GameState):

    def enter(self):
        #create a sprite
        mySprite = Sprite()
        mySprite.load_anim("nesFighter")
        mySprite.set_anim("nesFighter")
        mySprite.set_frame_tag("Idle")

        self.mySprite = mySprite

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        if Action.START in actions: # if any action was pressed
            self.gamestate_manager.change_state("playing")
        elif Action.A in actions:
            self.gamestate_manager.change_state("playing")

    def update(self, dt):
        self.mySprite.update(dt)
        

    def draw(self):
        font = pygame.font.SysFont(None, 32)
        text = font.render("MENU - Press Enter", True, (255, 255, 255))
        self.view_manager.game_surface.blit(text, (0, 0))

        self.mySprite.draw(self.view_manager.game_surface, world_pos=(0, 0))

    def debug_draw(self):
        self.mySprite.debug_draw(self.view_manager.debug_surface, world_pos=(0, 0))

