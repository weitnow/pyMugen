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

        self._draw_rect = pygame.Rect(0, 0, 0, 0)  # Initialize the draw rect for reuse

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

    def draw_rect(self, x, y, width, height, color):
        self._draw_rect.topleft = (x, y)
        self._draw_rect.size = (width, height)
        pygame.draw.rect(self.game_surface, color, self._draw_rect)

    def draw_rect_outline(self, x, y, width, height, color, thickness=1):
        self._draw_rect.topleft = (x, y)
        self._draw_rect.size = (width, height)
        pygame.draw.rect(self.game_surface, color, self._draw_rect, thickness)

  
    def draw_circle(self, x, y, radius, color):
        pygame.draw.circle(self.game_surface, color, (x, y), radius)

    def draw_circle_outline(self, x, y, radius, color, thickness=1):
        pygame.draw.circle(self.game_surface, color, (x, y), radius, thickness)