import pygame

class Camera:
    def __init__(self, view_width, view_height, world_width, world_height):
        self.view_width = view_width
        self.view_height = view_height

        self.world_width = world_width
        self.world_height = world_height

        self.x = 0
        self.y = 0

        self.smooth_speed = 0.1

    def update(self, p1, p2):
        # --- midpoint ---
        mid_x = (p1.pos.x + p2.pos.x) / 2
        mid_y = (p1.pos.y + p2.pos.y) / 2

        # --- horizontal ---
        target_x = mid_x - self.view_width / 2

        # --- vertical (minimal movement) ---
        jump_offset = 0
        if not p1.on_ground or not p2.on_ground:
            jump_offset = -20  # smaller than before for your low resolution

        target_y = mid_y - self.view_height / 2 + jump_offset

        # --- clamp ---
        target_x = max(0, min(target_x, self.world_width - self.view_width))
        target_y = max(0, min(target_y, self.world_height - self.view_height))

        # --- smooth --- #TODO: uncomment both lines below
        #self.x += (target_x - self.x) * self.smooth_speed
        #self.y += (target_y - self.y) * self.smooth_speed

    def apply(self, rect):
        return rect.move(-self.x, -self.y)
    
    def apply_vec2(self, pos):
        return pygame.Vector2(pos) - pygame.Vector2(self.x, self.y)