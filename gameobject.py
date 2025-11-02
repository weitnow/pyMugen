import pygame
from ressourcemanager import ResourceManager
from animationdata import AnimationData

class GameObject:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.animations: dict[str, AnimationData] = {}
        self.current_anim: AnimationData | None = None
        self.visible = True

        self.hurtbox: pygame.Rect | None = None
        self.hitbox: pygame.Rect | None = None

    # --- Animation Management ---
    def get_anim(self, name: str):
        rm = ResourceManager()
        if name not in self.animations:
            self.animations[name] = rm.get_animation_instance(name)

    def set_anim(self, name: str):
        if name in self.animations:
            self.current_anim = self.animations[name]

    def set_frame_tag(self, tag_name: str):
        if self.current_anim:
            self.current_anim.set_tag(tag_name)

    def set_frame(self, frame_index: int):
        if self.current_anim:
            self.current_anim.set_frame(frame_index)

    def update(self, dt: int):
        if self.current_anim:
            self.current_anim.update(dt)

    def draw(self, surface: pygame.Surface):
        if not self.visible or not self.current_anim:
            return
        frame = self.current_anim.get_current_frame()
        surface.blit(frame, self.pos)

    # --- Debug helpers ---
    def set_hitbox(self, rect: pygame.Rect):
        self.hitbox = rect

    def set_hurtbox(self, rect: pygame.Rect):
        self.hurtbox = rect

    def draw_debug(self, debug_surface: pygame.Surface, to_debug_coords):
        if self.hurtbox:
            x, y = to_debug_coords(self.hurtbox.x + self.pos.x, self.hurtbox.y + self.pos.y)
            w = self.hurtbox.width * 8
            h = self.hurtbox.height * 8
            pygame.draw.rect(debug_surface, (0, 0, 255, 180), (x, y, w, h), 2)

        if self.hitbox:
            x, y = to_debug_coords(self.hitbox.x + self.pos.x, self.hitbox.y + self.pos.y)
            w = self.hitbox.width * 8
            h = self.hitbox.height * 8
            pygame.draw.rect(debug_surface, (255, 0, 0, 180), (x, y, w, h), 2)
