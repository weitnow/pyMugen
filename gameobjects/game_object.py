import pygame
import globals
from resource_manager import ResourceManager
from resource_manager import AnimationData
from debug_manager import DebugManager


class GameObject:
    def __init__(self, pos: tuple[float, float], rotatable: bool = False):
        # Transform
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.current_angle = 0  # use set_rotation() to change
        self.flip_x = False
        self.flip_y = False
        
        # State
        self.visible = True     # call draw() or not
        self.active = True      # call update() or not
        self.rotatable = rotatable 
        self.on_ground = True
        self.origin_center_bottom = False

        # Physics constants
        self.speed = 0.1
        self.jump_velocity = -0.4
        self.gravity = 0.001  # TODO: move to globals or physics manager
        self.ground_y = 140   # TODO: move to globals or physics manager
        
        # Animation
        self.animations: dict[str, AnimationData] = {}      # holds AniationDate for example gbFighter, nesFighter, etc.
        self.current_anim: AnimationData | None = None      # current AnimationData being used

        # Collision
        self.hurtbox: pygame.Rect | None = None
        self.hitbox: pygame.Rect | None = None
        
        # Cached resource manager reference
        self._rm = ResourceManager()
        self._debug_manager = DebugManager()

    # -----------------------
    # Animation Management
    # -----------------------
    def get_anim(self, name: str) -> AnimationData:
        """Get or create animation instance."""
        if name not in self.animations:
            self.animations[name] = self._rm.get_animation_instance(name)
        return self.animations[name]

    def set_anim(self, name: str) -> bool:
        """Set current animation. Returns True if successful."""
        if name in self.animations:
            self.current_anim = self.animations[name]
            return True
        #log a warning here
        print(f"Warning: Animation '{name}' not found in GameObject.")
        return False

    def set_frame_tag(self, tag_name: str):
        """Set animation to specific tag."""
        if self.current_anim:
            self.current_anim.set_tag(tag_name)

    def set_frame(self, frame_index: int):
        """Set animation to specific frame."""
        if self.current_anim:
            self.current_anim.set_frame(frame_index)

    # -----------------------
    # Update
    # -----------------------
    def update(self, dt: int):
        """Update physics and animation."""
        if not self.active:
            return
        
        self._update_physics(dt)
        self._update_animation(dt)

    def _update_physics(self, dt: int):
        """Handle gravity and ground collision."""
        # Apply gravity
        self.vel.y += self.gravity * dt
        self.pos.y += self.vel.y * dt

        # Ground collision
        if self.pos.y >= self.ground_y:
            self.pos.y = self.ground_y
            self.vel.y = 0
            self.on_ground = True

    def _update_animation(self, dt: int):
        """Update current animation frame."""
        if self.current_anim:
            self.current_anim.update(dt)

    # -----------------------
    # Rotation + Flipping
    # -----------------------
    def set_rotation(self, angle: float):
        """Set rotation angle in 45° increments."""
        if not self.rotatable:
            raise ValueError("This GameObject is not rotatable.")
        
        # Validate angle is in 45° increments
        if angle % 45 != 0:
            raise ValueError("Angle must be in 45 degree increments")
        
        self.current_angle = (round(angle / 45) * 45) % 360

    def set_flip(self, flip_x: bool = False, flip_y: bool = False):
        """Set horizontal and/or vertical flip."""
        self.flip_x = flip_x
        self.flip_y = flip_y

    # -----------------------
    # Origin / Positioning
    # -----------------------
    def _compute_origin_offset(self, image: pygame.Surface) -> pygame.Vector2:
        """Calculate offset based on origin mode."""
        if not self.origin_center_bottom:
            return pygame.Vector2(0, 0)
        
        w, h = image.get_size()
        return pygame.Vector2(-w / 2, -h)

    def get_draw_position(self, image: pygame.Surface) -> pygame.Vector2:
        """Get final draw position with origin offset applied."""
        return self.pos + self._compute_origin_offset(image)

    # -----------------------
    # Drawing
    # -----------------------
    def draw(self, surface: pygame.Surface):
        """Draw the game object."""
        if not self._should_draw():
            return

        frame = self._get_transformed_frame()
        if frame:
            surface.blit(frame, self.get_draw_position(frame))

    def _should_draw(self) -> bool:
        """Check if object should be drawn."""
        return self.visible and self.active and self.current_anim is not None

    def _get_transformed_frame(self) -> pygame.Surface | None:
        """Get current frame with rotation/flip applied."""
        if not self.current_anim:
            return None

        frame = self.current_anim.get_current_frame()
        
        # Handle rotation (uses shared cache via ResourceManager)
        if self.rotatable:
            frame = self._get_rotated_frame(frame)
        # Handle flipping
        elif self.flip_x or self.flip_y:
            frame = pygame.transform.flip(frame, self.flip_x, self.flip_y)

        return frame

    def _get_rotated_frame(self, base_frame: pygame.Surface) -> pygame.Surface:
        """Get rotated frame from cache or generate it."""
        frame_idx = self.current_anim.current_frame_idx
        base_name = getattr(self.current_anim, "base_name", None)
        
        # Use shared ResourceManager cache
        return self._rm.get_rotated_frame(base_name, frame_idx, self.current_angle, self.flip_x, self.flip_y)
            

    # -----------------------
    # Hitbox / Hurtbox
    # -----------------------
    def set_hitbox(self, rect: pygame.Rect, relative_to_origin: bool = True):
        """Set hitbox rectangle."""
        self.hitbox = self._store_relative_rect(rect, relative_to_origin)

    def set_hurtbox(self, rect: pygame.Rect, relative_to_origin: bool = True):
        """Set hurtbox rectangle."""
        self.hurtbox = self._store_relative_rect(rect, relative_to_origin)

    def _store_relative_rect(self, rect: pygame.Rect, relative_to_origin: bool) -> pygame.Rect:
        """Store rect relative to origin if needed."""
        if relative_to_origin:
            return rect.copy()
        
        if not self.current_anim:
            return rect.copy()
        
        offset = self._compute_origin_offset(self.current_anim.get_current_frame())
        return rect.move(-int(offset.x), -int(offset.y))

    # -----------------------
    # Debug Drawing
    # -----------------------
    def draw_debug(self, debug_surface: pygame.Surface, to_debug_coords):
        """Draw debug overlays for hitboxes and bounding boxes."""
        if not self._debug_manager.debug_on:
            return

        frame = self.current_anim.get_current_frame() if self.current_anim else None
        offset = self._compute_origin_offset(frame) if frame else pygame.Vector2(0, 0)
        scale = globals.DEBUG_SCALE

        # Draw bounding box
        if frame and self._debug_manager.SHOW_BOUNDING_BOXES:
            frame_rect = pygame.Rect(
                self.pos.x + offset.x,
                self.pos.y + offset.y,
                *frame.get_size()
            )
            self._debug_manager.draw_bounding_box(
                debug_surface, frame_rect, to_debug_coords,
                scale, self.origin_center_bottom
            )

        # Draw hurtbox
        if self.hurtbox and self._debug_manager.SHOW_HURTBOXES:
            adjusted_rect = self.hurtbox.move(int(offset.x), int(offset.y))
            self._debug_manager.draw_hitbox(
                debug_surface, adjusted_rect, (0, 0, 255, 180),
                to_debug_coords, scale, self.pos
            )

        # Draw hitbox
        if self.hitbox and self._debug_manager.SHOW_HITBOXES:
            adjusted_rect = self.hitbox.move(int(offset.x), int(offset.y))
            self._debug_manager.draw_hitbox(
                debug_surface, adjusted_rect, (255, 0, 0, 180),
                to_debug_coords, scale, self.pos
            )