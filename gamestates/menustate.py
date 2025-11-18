import pygame
from gamestates.gamestate import GameState

class MenuState(GameState):

    def enter(self):
        pass

    def exit(self):
        pass


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.change_state("playing")

    def update(self, dt):
        pass

    def draw(self, surface):
   
        font = pygame.font.SysFont(None, 32)
        text = font.render("MENU - Press Enter", True, (255, 255, 255))
        surface.blit(text, (0, 0))