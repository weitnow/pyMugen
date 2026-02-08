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
        
        # --- Debug Toggles ---
        self.debug_on = True
        self.stop_game_for_debugging = False
        self.SHOW_HITBOXES = True
        self.SHOW_HURTBOXES = True
        self.SHOW_BOUNDING_BOXES = True
        self.SHOW_FPS_SYSTEM_INFO = True
        
        # For CPU/Memory updates - cache these
        self.last_system_info_update = 0
        self.system_info_update_interval = 3.0  # update every 3 seconds
        self.cpu_percent = 0
        self.mem_used_mb = 0
        
        # Cache the process object instead of creating it every frame
        self.process = psutil.Process()

    def set_view_manager(self, view_manager):   # gets called from view manager after its creation, to inform debug manager about it
        self.view_manager = view_manager

    def update(self, dt):
        if not self.debug_on:
            return
            
        now = time.time()
        self.frame_time_ms = dt * 1000.0
        if now - self.last_time > 0:
            self.fps = 1.0 / dt if dt > 0 else 0
            self.last_time = now
        
        # Only update system info at the specified interval
        if now - self.last_system_info_update >= self.system_info_update_interval:
            self._update_system_info()
            self.last_system_info_update = now

    def debug_draw(self):
        if not self.debug_on:
            return
        self._draw_fps_systeminfo(self.view_manager.debug_surface)

    def _draw_fps_systeminfo(self, surface):
        if not self.SHOW_FPS_SYSTEM_INFO:
            return
        
        # Use cached values instead of calling psutil every frame
        text = f"FPS: {self.fps:.1f} | CPU: {self.cpu_percent:.1f}% | RAM: {self.mem_used_mb:.1f} MB"
        img = self.font.render(text, True, (255, 255, 255))
        surface.blit(img, (4, 4))

    def _update_system_info(self):
        # Get CPU percentage (non-blocking, uses cached value from psutil)
        self.cpu_percent = self.process.cpu_percent()
        
        # Get memory info
        mem_info = self.process.memory_info()
        self.mem_used_mb = mem_info.rss / (1024 * 1024)

        # --- Debug Drawing Helpers ---
    def draw_rect_game(self, pos, width, height, color):
        """Draw a rectangle using game-space coordinates automatically scaled to debug coords."""
        if not self.debug_on or self.view_manager is None:
            return

        # Convert position using ViewManager scaling
        dx, dy = self.view_manager.to_debug_coords(pos[0], pos[1])

        # Convert rect size
        dw, dh = self.view_manager.to_debug_coords(width, height)

        pygame.draw.rect(
            self.view_manager.debug_surface,
            color,
            pygame.Rect(dx, dy, dw, dh),
            self.BOX_THICKNESS
        )

    def draw_circle_game(self, x, y, radius, color):
        """Draw a circle using game-space coordinates automatically scaled to debug coords."""
        if not self.debug_on or self.view_manager is None:
            return

        dx, dy = self.view_manager.to_debug_coords(x, y)
        dr, _ = self.view_manager.to_debug_coords(radius, radius)

        pygame.draw.circle(
            self.view_manager.debug_surface,
            color,
            (int(dx), int(dy)),
            int(dr),
            self.BOX_THICKNESS
        )

    def draw_line_game(self, x1, y1, x2, y2, color):
        """Draw a line using game-space coordinates automatically scaled to debug coords."""
        if not self.debug_on or self.view_manager is None:
            return

        dx1, dy1 = self.view_manager.to_debug_coords(x1, y1)
        dx2, dy2 = self.view_manager.to_debug_coords(x2, y2)

        pygame.draw.line(
            self.view_manager.debug_surface,
            color,
            (dx1, dy1),
            (dx2, dy2),
            self.BOX_THICKNESS
        )

    def draw_text_game(self, x, y, text, color):
        """Draw text using game-space coordinates automatically scaled to debug coords."""
        if not self.debug_on or self.view_manager is None:
            return

        dx, dy = self.view_manager.to_debug_coords(x, y)

        img = self.font.render(text, True, color)
        self.view_manager.debug_surface.blit(img, (dx, dy))

    def draw_text_debug(self, x, y, text, color):
        """Draw text directly in debug-surface coordinates (no scaling)."""
        if not self.debug_on or self.view_manager is None:
            return

        img = self.font.render(text, True, color)
        self.view_manager.debug_surface.blit(img, (x, y))

