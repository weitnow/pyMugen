import pygame
from gamestates.gamestate import GameState

class PlayingState(GameState):
    def draw(self, surface):
        surface.fill((0, 100, 200))
        font = pygame.font.SysFont(None, 50)
        text = font.render("PLAYING - Press Esc to Menu", True, (255, 255, 255))
        surface.blit(text, (50, 100))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.change_state("menu")