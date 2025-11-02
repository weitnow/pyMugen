import pygame
import time

class DebugManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DebugManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.show_hitboxes = True
        self.show_hurtboxes = True
        self.show_bounding_boxes = False
        self.show_fps_info = True
        self.font = pygame.font.Font(None, 14)
        self.last_time = time.time()
        self.fps = 0
        self.frame_time_ms = 0

    # --- Toggles ---
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.show_hitboxes = not self.show_hitboxes
            elif event.key == pygame.K_F2:
                self.show_hurtboxes = not self.show_hurtboxes
            elif event.key == pygame.K_F3:
                self.show_bounding_boxes = not self.show_bounding_boxes
            elif event.key == pygame.K_F4:
                self.show_fps_info = not self.show_fps_info

    def update_timing(self, dt):
        now = time.time()
        self.frame_time_ms = dt
        if now - self.last_time > 0:
            self.fps = 1000.0 / dt if dt > 0 else 0
        self.last_time = now

    def draw_fps(self, surface):
        if not self.show_fps_info:
            return
        text = f"FPS: {self.fps:.1f}  Frame: {self.frame_time_ms:.1f}ms"
        img = self.font.render(text, True, (255, 255, 255))
        surface.blit(img, (4, 4))

    # --- Drawing ---
    def draw_hitbox(self, surface, rect: pygame.Rect, color, to_debug_coords, scale, pos):
        x, y = to_debug_coords(rect.x + pos.x, rect.y + pos.y)
        w, h = rect.width * scale, rect.height * scale
        pygame.draw.rect(surface, color, (x, y, w, h), 2)

    def draw_bounding_box(self, surface, sprite_rect, to_debug_coords, scale):
        x, y = to_debug_coords(sprite_rect.x, sprite_rect.y)
        w, h = sprite_rect.width * scale, sprite_rect.height * scale
        pygame.draw.rect(surface, (255, 255, 0, 120), (x, y, w, h), 1)

    def draw_text(self, surface, text, x, y):
        img = self.font.render(text, True, (255, 255, 255))
        surface.blit(img, (x, y))
