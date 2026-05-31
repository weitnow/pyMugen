import pygame
from decorators import singleton
from managers.debug_manager import DebugManager
from managers.view_manager.camera import Camera

@singleton
class ViewManager:
    def __init__(self):
        self._sp = None  # set by ServiceProvider after all managers are initialized
        self.debug_manager = None  # set in bind_service_provider

        self.GAME_WINDOW_WIDTH = 960
        self.GAME_WINDOW_HEIGHT = 540


        self.VIEW_LEFT_BOUND = 94 #first visible pixel on the left
        self.VIEW_RIGHT_BOUND = 868 #first visible pixel on the right
        self.VIEW_WIDTH = self.VIEW_RIGHT_BOUND - self.VIEW_LEFT_BOUND # 774
   
        self.VIEW_TOP_BOUND = 86 #first visible pixel on the up
        self.VIEW_BOTTOM_BOUND = 454 #first visible pixel on the down
        self.VIEW_HEIGHT = self.VIEW_BOTTOM_BOUND - self.VIEW_TOP_BOUND # 368
    
        

        self.CLEAR_COLOR = (30, 30, 30)

        self._draw_rect = pygame.Rect(0, 0, 0, 0)  # Initialize the draw rect for reuse

        self.camera = Camera(self.VIEW_WIDTH, self.VIEW_HEIGHT) 

        self.screen = pygame.display.set_mode(
            (self.GAME_WINDOW_WIDTH, self.GAME_WINDOW_HEIGHT),
            pygame.SCALED | pygame.FULLSCREEN,
            vsync=1
        )
        pygame.display.set_caption("Game View")

        self.game_surface = pygame.Surface((self.GAME_WINDOW_WIDTH, self.GAME_WINDOW_HEIGHT))

        

    def bind_service_provider(self, sp):
        self._sp = sp
        self.debug_manager = sp.debug_manager
        

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