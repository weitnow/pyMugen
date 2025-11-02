import pygame
import globals
from ressourcemanager import ResourceManager
from animationdata import AnimationData
from debugmanager import DebugManager


class GameObject:
    def __init__(self, pos: tuple[float, float]):
        self.pos = pygame.Vector2(pos)
        self.visible = True

        self.animations: dict[str, AnimationData] = {}
        self.current_anim: AnimationData | None = None

        # hitboxes stored relative to origin
        self.hurtbox: pygame.Rect | None = None
        self.hitbox: pygame.Rect | None = None

        # False = top-left, True = center-bottom
        self.origin_center_bottom: bool = False

    # -----------------------
    # Animation Management
    # -----------------------
    def get_anim(self, name: str):
        rm = ResourceManager()
        if name not in self.animations:
            self.animations[name] = rm.get_animation_instance(name)
        return self.animations[name]

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

    # -----------------------
    # Origin / Positioning
    # -----------------------
    def _compute_origin_offset(self) -> pygame.Vector2:
        """Returns the offset to apply based on origin mode."""
        offset = pygame.Vector2(0, 0)
        if self.origin_center_bottom and self.current_anim:
            w, h = self.current_anim.get_current_frame().get_size()
            offset.x = -w / 2
            offset.y = -h
        return offset

    def get_draw_position(self) -> pygame.Vector2:
        """Returns the actual top-left position for blitting."""
        return self.pos + self._compute_origin_offset()

    # -----------------------
    # Drawing
    # -----------------------
    def draw(self, surface: pygame.Surface):
        if not self.visible or not self.current_anim:
            return
        frame = self.current_anim.get_current_frame()
        surface.blit(frame, self.get_draw_position())

    # -----------------------
    # Hitbox / Hurtbox
    # -----------------------
    def set_hitbox(self, rect: pygame.Rect, relative_to_origin: bool = True):
        self.hitbox = self._store_relative_rect(rect, relative_to_origin)

    def set_hurtbox(self, rect: pygame.Rect, relative_to_origin: bool = True):
        self.hurtbox = self._store_relative_rect(rect, relative_to_origin)

    def _store_relative_rect(self, rect: pygame.Rect, relative_to_origin: bool) -> pygame.Rect:
        """Stores a rectangle relative to the object's origin."""
        if relative_to_origin:
            return rect.copy()
        else:
            offset = self._compute_origin_offset()
            return rect.move(-offset)

    # -----------------------
    # Debug drawing
    # -----------------------
    def draw_debug(self, debug_surface, to_debug_coords):
        debug = DebugManager()
        scale = globals.DEBUG_SCALE
        offset = self._compute_origin_offset()

        if self.hurtbox and globals.show_hurtboxes:
            debug.draw_hitbox(debug_surface, self.hurtbox.move(offset),
                              (0, 0, 255, 180), to_debug_coords, scale, self.pos)

        if self.hitbox and globals.show_hitboxes:
            debug.draw_hitbox(debug_surface, self.hitbox.move(offset),
                              (255, 0, 0, 180), to_debug_coords, scale, self.pos)

        if self.current_anim and globals.show_bounding_boxes:
            frame_rect = pygame.Rect(
                self.pos.x + offset.x,
                self.pos.y + offset.y,
                *self.current_anim.get_current_frame().get_size()
            )
            debug.draw_bounding_box(debug_surface, frame_rect, to_debug_coords, scale)
