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
        self.show_overlay = False
        self.debug_on = True
        self.stop_game_for_debugging = False
        self.SHOW_HITBOXES = True
        self.SHOW_HURTBOXES = True
        self.SHOW_BOUNDING_BOXES = True
        self.SHOW_FPS_INFO = True
        
        # For CPU/Memory updates - cache these
        self.last_system_info_update = 0
        self.system_info_update_interval = 3.0  # update every 3 seconds
        self.cpu_percent = 0
        self.mem_used_mb = 0
        
        # Cache the process object instead of creating it every frame
        self.process = psutil.Process()

    def set_view_manager(self, view_manager):
        self.view_manager = view_manager

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.debug_on = not self.debug_on
            elif event.key == pygame.K_F2:
                self.stop_game_for_debugging = not self.stop_game_for_debugging
            elif event.key == pygame.K_F3:
                self.show_overlay = not self.show_overlay

    def update(self, dt):
        if not self.debug_on:
            return
            
        now = time.time()
        self.frame_time_ms = dt
        if now - self.last_time > 0:
            self.fps = 1000.0 / dt if dt > 0 else 0
            self.last_time = now
        
        # Only update system info at the specified interval
        if now - self.last_system_info_update >= self.system_info_update_interval:
            self.update_system_info()
            self.last_system_info_update = now

    def debug_draw(self):
        if not self.debug_on:
            return
        self._draw_fps(self.view_manager.debug_surface)

    def _draw_fps(self, surface):
        if not self.SHOW_FPS_INFO:
            return
        
        # Use cached values instead of calling psutil every frame
        text = f"FPS: {self.fps:.1f} | CPU: {self.cpu_percent:.1f}% | RAM: {self.mem_used_mb:.1f} MB"
        img = self.font.render(text, True, (255, 255, 255))
        surface.blit(img, (4, 4))

    def update_system_info(self):
        # Get CPU percentage (non-blocking, uses cached value from psutil)
        self.cpu_percent = self.process.cpu_percent()
        
        # Get memory info
        mem_info = self.process.memory_info()
        self.mem_used_mb = mem_info.rss / (1024 * 1024)

    def draw_hitbox(self, surface, rect: pygame.Rect, color, to_debug_coords, scale, pos):
        if not self.debug_on or not self.SHOW_HITBOXES:
            return
        x, y = to_debug_coords(rect.x + pos.x, rect.y + pos.y)
        w, h = rect.width * scale, rect.height * scale
        pygame.draw.rect(surface, color, (x, y, w, h), self.BOX_THICKNESS)

    def draw_bounding_box(self, surface, sprite_rect, to_debug_coords, scale, origin_center_bottom=False):
        if not self.debug_on or not self.SHOW_BOUNDING_BOXES:
            return
        x, y = to_debug_coords(sprite_rect.x, sprite_rect.y)
        w, h = sprite_rect.width * scale, sprite_rect.height * scale
        pygame.draw.rect(surface, (255, 255, 0, 120), (x, y, w, h), self.BOX_THICKNESS)
        
        if origin_center_bottom:
            origin_x = sprite_rect.x + sprite_rect.width / 2
            origin_y = sprite_rect.y + sprite_rect.height
        else:
            origin_x = sprite_rect.x
            origin_y = sprite_rect.y
        ox, oy = to_debug_coords(origin_x, origin_y)
        pygame.draw.circle(surface, (0, 255, 0), (int(ox), int(oy)), 3)

    def draw_text(self, surface, text, x, y):
        if not self.debug_on:
            return
        img = self.font.render(text, True, (255, 255, 255))
        surface.blit(img, (x, y))