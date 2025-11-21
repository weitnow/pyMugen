import pygame
from resource_manager import ResourceManager, AnimationData
from debug_manager import DebugManager
import globals

class Sprite:
    def __init__(self):
        # PUBLIC attributes (with property access)
        self._flip_x: bool = False
        self._flip_y: bool = False
        self._offset: pygame.Vector2 = pygame.Vector2(0, 0) # this is only used if sprite is attached to a GameObject!
        self._rotation: int = 0
        
        # PUBLIC read-only attributes
        self.sprite_size = (0, 0)  # (width, height)


        # Private attributes
        self._rm: ResourceManager = ResourceManager()
        self._dm: DebugManager = DebugManager()
        self._animations: dict[str, AnimationData] = {}
        self._current_anim: AnimationData | None = None
        
    # ---------------------
    # Properties
    # ---------------------
    @property
    def flip_x(self) -> bool:
        """Flip sprite horizontally."""
        return self._flip_x

    @flip_x.setter
    def flip_x(self, value: bool):
        self._flip_x = bool(value)

    @property
    def flip_y(self) -> bool:
        """Flip sprite vertically."""
        return self._flip_y

    @flip_y.setter
    def flip_y(self, value: bool):
        self._flip_y = bool(value)

    @property
    def offset(self) -> pygame.Vector2:
        """Offset applied when drawing sprite."""
        return self._offset

    @offset.setter
    def offset(self, value: pygame.Vector2):
        if not isinstance(value, pygame.Vector2):
            raise TypeError("offset must be a pygame.Vector2")
        self._offset = value

    @property
    def rotation(self) -> int:
        """Current rotation in 45° increments."""
        return self._rotation

    @rotation.setter
    def rotation(self, angle: int):
        self._rotation = int(angle) % 360

    # ---------------------
    # Animation methods
    # ---------------------
    def load_anim(self, name: str):
        """Retrieve an animation instance by name."""
        if name not in self._animations:
            self._animations[name] = self._rm.get_animation_instance(name)
        

    def set_anim(self, name: str):
        """Set the current animation."""
        if name in self._animations:
            self._current_anim = self._animations[name]
        #update sprite size
        anim = self._animations[name]
        self.sprite_size = anim.sprite_size


    def set_frame_tag(self, tag_name: str):
        """Set animation to specific tag."""
        if self._current_anim:
            self._current_anim.set_tag(tag_name)

    def set_frame(self, frame_index: int):
        """Set animation to specific frame."""
        if self._current_anim:
            self._current_anim.set_frame(frame_index)

    # ---------------------
    # Update / Draw
    # ---------------------
    def update(self, dt: int):
        """Update current animation frame."""
        if self._current_anim:
            self._current_anim.update(dt)

    def draw(self, surface: pygame.Surface, world_pos: pygame.Vector2 | tuple[int, int]):
        """Draw the sprite to a surface with current transforms and offsets applied."""
        if not self._current_anim:
            return

        # Ensure world_pos is a Vector2
        pos = pygame.Vector2(world_pos)

        # Apply additive offset from animation
        offset = self._current_anim.get_current_offset()
        draw_pos = pos + pygame.Vector2(offset)

        # Get transformed frame (rotation + flip applied)
        frame = self._get_transformed_frame()
        if frame:
            surface.blit(frame, draw_pos)

    # ---------------------
    # Debug Draw
    # ---------------------

    def debug_draw(self, surface: pygame.Surface, world_pos: pygame.Vector2 | tuple[int, int]):
        """Draw debug info for the sprite."""
        if not self._current_anim:
            return

        # Ensure world_pos is a Vector2
        pos = pygame.Vector2(world_pos)

        # --- Draw bounding box without offset ---
        self._dm.draw_rect_game(pos, self.sprite_size[0], self.sprite_size[1], globals.COLOR_LIGHT_GRAY)

        # --- Draw bounding box with additive offsets applied ---
        offset = self._current_anim.get_current_offset()
        offset_pos = pos + pygame.Vector2(offset)
        self._dm.draw_rect_game(offset_pos, self.sprite_size[0], self.sprite_size[1], globals.COLOR_DARK_GRAY)



    

    # ---------------------
    # Private helpers
    # ---------------------
    def _get_transformed_frame(self) -> pygame.Surface | None:
        """Get current animation frame with rotation/flip applied."""
        if not self._current_anim:
            return None

        frame = self._current_anim.get_current_frame()

        # Handle rotation
        if self._rotation != 0:
            frame = self._get_rotated_frame(frame)
        # Handle flipping
        elif self._flip_x or self._flip_y:
            frame = pygame.transform.flip(frame, self._flip_x, self._flip_y)

        return frame

    def _get_rotated_frame(self, base_frame: pygame.Surface) -> pygame.Surface:
        """Get rotated frame from cache or generate it, snapping to 45° increments."""
        frame_idx = self._current_anim.current_frame_idx
        base_name = getattr(self._current_anim, "base_name", None)
        
        # Snap rotation for caching/drawing
        snapped_angle = round(self._rotation / 45) * 45 % 360
        
        return self._rm.get_rotated_frame(base_name, frame_idx, snapped_angle, self._flip_x, self._flip_y)