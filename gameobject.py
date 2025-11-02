import pygame
import globals
from ressourcemanager import ResourceManager
from animationdata import AnimationData
from debugmanager import DebugManager


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

    def draw_debug(self, debug_surface, to_debug_coords):
        debug = DebugManager()
        scale = globals.DEBUG_SCALE

        if self.hurtbox and globals.show_hurtboxes:
            debug.draw_hitbox(debug_surface, self.hurtbox, (0, 0, 255, 180), to_debug_coords, scale, self.pos)

        if self.hitbox and globals.show_hitboxes:
            debug.draw_hitbox(debug_surface, self.hitbox, (255, 0, 0, 180), to_debug_coords, scale, self.pos)

        if self.current_anim and globals.show_bounding_boxes:
            frame_rect = pygame.Rect(self.pos.x, self.pos.y, *self.current_anim.get_current_frame().get_size())
            debug.draw_bounding_box(debug_surface, frame_rect, to_debug_coords, scale)

     
