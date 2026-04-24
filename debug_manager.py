import pygame
import time
import psutil
from decorators import singleton

@singleton
class DebugManager:
    def __init__(self):
        self.font = pygame.font.Font(None, 20)
        self.last_time = time.time()
        self.fps = 0
        self.frame_time_ms = 0
        self.view_manager = None
        self.BOX_THICKNESS = 2
        
        self.debug_on = True
        self.SHOW_HITBOXES = True
        self.SHOW_HURTBOXES = True
        self.SHOW_BOUNDING_BOXES = True
        self.SHOW_FPS_SYSTEM_INFO = True
        self.SHOW_SPRITE_BOUNDS = True
        
        self.last_system_info_update = 0
        self.system_info_update_interval = 3.0
        self.cpu_percent = 0
        self.mem_used_mb = 0
        self.process = psutil.Process()

    def set_view_manager(self, view_manager):
        self.view_manager = view_manager

    def update(self, dt):
        if not self.debug_on:
            return
        now = time.time()
        self.frame_time_ms = dt * 1000.0
        self.fps = 1.0 / dt if dt > 0 else 0
        self.last_time = now
        if now - self.last_system_info_update >= self.system_info_update_interval:
            self._update_system_info()
            self.last_system_info_update = now

    def debug_draw(self):
        if not self.debug_on:
            return
        if self.SHOW_FPS_SYSTEM_INFO:
            self._draw_fps_systeminfo()

    def _draw_fps_systeminfo(self):
        text = f"FPS: {self.fps:.1f} | CPU: {self.cpu_percent:.1f}% | RAM: {self.mem_used_mb:.1f} MB"
        self._draw_text_screen((4, 4), text, (255, 255, 0))

    def _update_system_info(self):
        self.cpu_percent = self.process.cpu_percent()
        mem_info = self.process.memory_info()
        self.mem_used_mb = mem_info.rss / (1024 * 1024)

    # --- Draw on game_surface (game-space coordinates) ---

    def draw_rect_game(self, pos, width, height, color):
        if not self.debug_on or self.view_manager is None:
            return
        pygame.draw.rect(
            self.view_manager.game_surface,
            color,
            pygame.Rect(pos[0], pos[1], width, height),
            self.BOX_THICKNESS
        )

    def draw_circle_game(self, x, y, radius, color):
        if not self.debug_on or self.view_manager is None:
            return
        pygame.draw.circle(
            self.view_manager.game_surface,
            color,
            (int(x), int(y)),
            int(radius),
            self.BOX_THICKNESS
        )

    def draw_line_game(self, x1, y1, x2, y2, color):
        if not self.debug_on or self.view_manager is None:
            return
        pygame.draw.line(
            self.view_manager.game_surface,
            color,
            (x1, y1),
            (x2, y2),
            self.BOX_THICKNESS
        )

    def draw_text_game(self, pos, text, color):
        if not self.debug_on or self.view_manager is None:
            return
        img = self.font.render(text, True, color)
        self.view_manager.game_surface.blit(img, pos)

    def draw_crossed_rect_game(self, pos, width, height, color):
        if not self.debug_on or self.view_manager is None:
            return
        self.draw_rect_game(pos, width, height, color)
        x1, y1 = pos[0], pos[1]
        x2, y2 = pos[0] + width, pos[1] + height
        pygame.draw.line(self.view_manager.game_surface, color, (x1, y1), (x2, y2), self.BOX_THICKNESS)
        pygame.draw.line(self.view_manager.game_surface, color, (x2, y1), (x1, y2), self.BOX_THICKNESS)

    # --- Draw directly on screen (bypasses SCALED layer) ---

    def _draw_text_screen(self, pos, text, color):
        if self.view_manager is None:
            return
        real_screen = pygame.display.get_surface()
        img = self.font.render(text, True, color)
        real_screen.blit(img, pos)

    def draw_text_screen(self, pos, text, color):
        """Public method to draw text at physical screen coordinates."""
        if not self.debug_on or self.view_manager is None:
            return
        self._draw_text_screen(pos, text, color)