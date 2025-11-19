# sprite.py
import pygame
from resource_manager import ResourceManager, AnimationData


class Sprite:
    def __init__(self, pos=(0, 0), rotatable=False):
        self.position = pygame.Vector2(pos) 
        self.flip_x = False
        self.flip_y = False
        self.rotatable = rotatable
        self.rotation = 0

        self._rm = ResourceManager()

        # Animation
        self.animations: dict[str, AnimationData] = {}
        self.current_anim: AnimationData | None = None


    # ---------------------
    # Getters / Setters
    # ---------------------
    

    # ---------------------
    # Animation
    # ---------------------
    def get_anim(self, name):
        if name not in self.animations:
            self.animations[name] = self._rm.get_animation_instance(name)
        return self.animations[name]

    def set_anim(self, name):
        if name in self.animations:
            self.current_anim = self.animations[name]

    def set_frame_tag(self, tag_name: str):
        """Set animation to specific tag."""
        if self.current_anim:
            self.current_anim.set_tag(tag_name)

    def set_frame(self, frame_index: int):
        """Set animation to specific frame."""
        if self.current_anim:
            self.current_anim.set_frame(frame_index)


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
    # Update
    # -----------------------
    def update(self, dt: int):
        """Update current animation frame."""
        if self.current_anim:
            self.current_anim.update(dt)


    # ---------------------
    # Drawing
    # ---------------------
    def draw(self, surface: pygame.Surface):
        if not self.current_anim:
            return

        frame = self._get_transformed_frame()
        if frame:
            surface.blit(frame, self.position)

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
