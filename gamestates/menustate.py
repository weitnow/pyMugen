import pygame
from gamestates.gamestate import GameState

class MenuState(GameState):
    def draw(self, surface):
        surface.fill((30, 30, 30))
        font = pygame.font.SysFont(None, 50)
        text = font.render("MENU - Press Enter to Play", True, (255, 255, 255))
        surface.blit(text, (100, 100))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.change_state("playing")