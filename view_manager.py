import pygame
from decorators import singleton
from debug_manager import DebugManager
from camera import Camera

@singleton
class ViewManager:
    def __init__(self):
        self.GAME_VIEW_WIDTH = 960
        self.GAME_VIEW_HEIGHT = 540
        self.CLEAR_COLOR = (30, 30, 30)

        self.camera = Camera(self.GAME_VIEW_WIDTH, self.GAME_VIEW_HEIGHT, 1000, 1000)

        self.screen = pygame.display.set_mode(
            (self.GAME_VIEW_WIDTH, self.GAME_VIEW_HEIGHT),
            pygame.SCALED | pygame.FULLSCREEN,
            vsync=1
        )
        pygame.display.set_caption("Game View")

        self.game_surface = pygame.Surface((self.GAME_VIEW_WIDTH, self.GAME_VIEW_HEIGHT))

        self.debug_manager = DebugManager()
        self.debug_manager.set_view_manager(self)

    def update(self, dt):
        pass

    def clear(self):
        self.game_surface.fill(self.CLEAR_COLOR)

    def draw_to_screen(self):
        self.screen.blit(self.game_surface, (0, 0))
        pygame.display.flip()