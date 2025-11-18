import pygame
from gamestates.gamestate_base import GameState
from input_manager import Action

class MenuState(GameState):

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        self._input_handling()
        

    def draw(self):
        font = pygame.font.SysFont(None, 32)
        text = font.render("MENU - Press Enter", True, (255, 255, 255))
        self.view.game_surface.blit(text, (0, 0))


    def _input_handling(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        if Action.START in actions: # if any action was pressed
            self.game_state_manager.change_state("playing")
        elif Action.A in actions:
            self.game_state_manager.change_state("playing")
        elif Action.B in actions:
            self.game_state_manager.change_state("playing_stresstest")