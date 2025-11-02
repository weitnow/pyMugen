import pygame

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
        self.show_frame_info = False
        self.font = pygame.font.Font(None, 12)

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
                self.show_frame_info = not self.show_frame_info

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
