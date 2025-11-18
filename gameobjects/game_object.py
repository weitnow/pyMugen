import pygame
import globals
from resource_manager import ResourceManager
from resource_manager import AnimationData
from debug_manager import DebugManager


class GameObject:
    def __init__(self, pos: tuple[float, float], rotatable: bool = False):
        self.pos = pygame.Vector2(pos)
        self.visible = True
        self.active = True
        self.rotatable = rotatable

        # Physics
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = True
        self.speed = 0.1
        self.jump_velocity = -0.4
        self.gravity =0.001 # TODO: move to globals or physics manager
        self.ground_y = 140  # TODO: move to globals or physics manager
        
        self.animations: dict[str, AnimationData] = {}
        self.current_anim: AnimationData | None = None

        self.hurtbox: pygame.Rect | None = None
        self.hitbox: pygame.Rect | None = None

        self.origin_center_bottom: bool = False

        # Rotation handled centrally via ResourceManager shared cache
        self.rotation_cache: dict[int, pygame.Surface] = {}
        self.flip_x = False
        self.flip_y = False
        self.current_angle = 0  # in degrees

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
        if not self.active:
            return
        
        # Gravity
        self.vel.y += self.gravity * dt
        self.pos.y += self.vel.y * dt

        # Ground collision
        if self.pos.y >= self.ground_y:
            self.pos.y = self.ground_y
            self.vel.y = 0
            self.on_ground = True

        
        if self.current_anim:
            self.current_anim.update(dt)

    # -----------------------
    # Rotation + Flipping
    # -----------------------
    def _build_rotation_cache(self, anim: AnimationData):
        # legacy per-object precompute kept for compatibility but not used by default.
        # Prefer using ResourceManager.get_rotated_frame(shared cache) instead.
        pass

    def set_rotation(self, angle: float):
        """Set the object’s rotation angle, snapped to nearest 45°."""
        if not self.rotatable:
            return
        # check input angle, can only be in 45 degree increments
        assert angle % 45 == 0, "Angle must be in 45 degree increments"
        self.current_angle = (round(angle / 45) * 45) % 360

    def set_flip(self, flip_x: bool = False, flip_y: bool = False):
        self.flip_x = flip_x
        self.flip_y = flip_y

    # -----------------------
    # Origin / Positioning
    # -----------------------
    def _compute_origin_offset(self, image: pygame.Surface) -> pygame.Vector2:
        offset = pygame.Vector2(0, 0)
        if self.origin_center_bottom:
            w, h = image.get_size()
            offset.x = -w / 2
            offset.y = -h
        return offset

    def get_draw_position(self, image: pygame.Surface) -> pygame.Vector2:
        return self.pos + self._compute_origin_offset(image)

    # -----------------------
    # Drawing
    # -----------------------
    def draw(self, surface: pygame.Surface):
        if not self.visible or not self.current_anim or not self.active:
            return

        frame = self.current_anim.get_current_frame()

        # If rotatable, fetch from cache
        if self.rotatable:
            frame_idx = self.current_anim.current_frame_idx
            rm = ResourceManager()
            base_name = getattr(self.current_anim, "base_name", None)
            if base_name is not None:
                frame = rm.get_rotated_frame(base_name, frame_idx, self.current_angle, self.flip_x, self.flip_y)
            else:
                # fallback: rotate on-the-fly (cached per-object) if we don't know anim name
                key = (frame_idx, self.current_angle, self.flip_x, self.flip_y)
                if key not in self.rotation_cache:
                    rotated = pygame.transform.rotate(frame, self.current_angle)
                    if self.flip_x or self.flip_y:
                        rotated = pygame.transform.flip(rotated, self.flip_x, self.flip_y)
                    self.rotation_cache[key] = rotated
                frame = self.rotation_cache[key]

        elif self.flip_x or self.flip_y:
            frame = pygame.transform.flip(frame, self.flip_x, self.flip_y)

        surface.blit(frame, self.get_draw_position(frame))

    # -----------------------
    # Hitbox / Hurtbox
    # -----------------------
    def set_hitbox(self, rect: pygame.Rect, relative_to_origin: bool = True):
        self.hitbox = self._store_relative_rect(rect, relative_to_origin)

    def set_hurtbox(self, rect: pygame.Rect, relative_to_origin: bool = True):
        self.hurtbox = self._store_relative_rect(rect, relative_to_origin)

    def _store_relative_rect(self, rect: pygame.Rect, relative_to_origin: bool) -> pygame.Rect:
        if relative_to_origin:
            return rect.copy()
        else:
            offset = self._compute_origin_offset(self.current_anim.get_current_frame())
            return rect.move(-offset)

    # -----------------------
    # Debug drawing
    # -----------------------
    def draw_debug(self, debug_surface, to_debug_coords):
        debug = DebugManager()
        scale = globals.DEBUG_SCALE

        frame = self.current_anim.get_current_frame() if self.current_anim else None
        offset = self._compute_origin_offset(frame) if frame else pygame.Vector2(0, 0)

        if self.hurtbox and globals.show_hurtboxes:
            debug.draw_hitbox(debug_surface, self.hurtbox.move(offset),
                              (0, 0, 255, 180), to_debug_coords, scale, self.pos)

        if self.hitbox and globals.show_hitboxes:
            debug.draw_hitbox(debug_surface, self.hitbox.move(offset),
                              (255, 0, 0, 180), to_debug_coords, scale, self.pos)

        if frame and globals.show_bounding_boxes:
            frame_rect = pygame.Rect(
                self.pos.x + offset.x,
                self.pos.y + offset.y,
                *frame.get_size()
            )
            debug.draw_bounding_box(debug_surface, frame_rect, to_debug_coords, scale, self.origin_center_bottom)
