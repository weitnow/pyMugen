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
        self.view_manager = None  # to be set externally

        # settings
        self.BOX_THICKNESS = 2

        # --- Debug Toggles ---
        self.show_overlay = True
        self.debug_on = False  # enable or disable debug features globally
        self.stop_game_for_debugging = False
        self.SHOW_HITBOXES = True
        self.SHOW_HURTBOXES = True
        self.SHOW_BOUNDING_BOXES = True
        self.SHOW_FPS_INFO = True

        # For CPU updates
        self.last_cpu_update_time = 0
        self.cpu_percent = 0

    def set_view_manager(self, view_manager):
        """Called by ViewManager after initialization"""
        self.view_manager = view_manager

    # --- Toggles ---
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.debug_on = not self.debug_on
            elif event.key == pygame.K_F2:
                self.stop_game_for_debugging = not self.stop_game_for_debugging
            elif event.key == pygame.K_F3:
                self.show_overlay = not self.show_overlay

    def update(self, dt):
        now = time.time()
        self.frame_time_ms = dt
        if now - self.last_time > 0:
            self.fps = 1000.0 / dt if dt > 0 else 0
        self.last_time = now
        self.update_system_info()

    def debug_draw(self):
        self._draw_fps(self.view_manager.debug_surface)

    def _draw_fps(self, surface):
        if not self.SHOW_FPS_INFO:
            return

        process = psutil.Process()
        mem_info = process.memory_info()
        mem_used_mb = mem_info.rss / (1024 * 1024)

        text = f"FPS: {self.fps:.1f} | CPU: {self.cpu_percent:.1f}% | RAM: {mem_used_mb:.1f} MB"
        img = self.font.render(text, True, (255, 255, 255))
        surface.blit(img, (4, 4))

    def update_system_info(self):
        now = time.time()
        if now - self.last_cpu_update_time > 5:  # update every 5 seconds
            self.cpu_percent = psutil.cpu_percent(interval=None)
            self.last_cpu_update_time = now

    # --- Drawing ---
    def draw_hitbox(self, surface, rect: pygame.Rect, color, to_debug_coords, scale, pos):
        x, y = to_debug_coords(rect.x + pos.x, rect.y + pos.y)
        w, h = rect.width * scale, rect.height * scale
        pygame.draw.rect(surface, color, (x, y, w, h), self.BOX_THICKNESS)

    def draw_bounding_box(self, surface, sprite_rect, to_debug_coords, scale, origin_center_bottom=False):
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
        img = self.font.render(text, True, (255, 255, 255))
        surface.blit(img, (x, y))
