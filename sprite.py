import pygame
from resource_manager import ResourceManager, AnimationData
from debug_manager import DebugManager

class Sprite:
    def __init__(self):
        # PUBLIC attributes (with property access)
        self._flip_x: bool = False
        self._flip_y: bool = False
        self._rotation: int = 0
        self._snapped_rotation: int = 0
        
        # Animation data
        self.frames = None  # is a Dict[int, pygame.Surface], is a reference to the origianal, reference, do NOT modify!
        self.frame_durations = None  # is a Dict[int, int] mapping frame index to duration in ms, reference, do NOT modify!
        self.tags = None  # is a Dict[str, Dict[str, int]] mapping tag name to {"from": int, "to": int}, reference, do NOT modify!
        self.final_offsets = None  # is a Dict[int, (x, y)], reference, do NOT modify!
        self.sprite_size = None  # is a tuple (width, height)
       
        self.base_name = None # is a str name of the current animation-file
        self.current_tag = None # is a str name of the current tag
        self.current_frame_idx = 0
        self.timer = 0
        self.playing = False
        self.png = False # True if this sprite is a single PNG, False if it is an animation
        
        # Private attributes
        self._rm: ResourceManager = ResourceManager()
        self._dm: DebugManager = DebugManager()
        
        
    # ---------------------
    # Properties

        # Determine ang
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
    def rotation(self) -> int:
        return self._rotation

    @rotation.setter
    def rotation(self, angle: int):
        self._rotation = int(angle) % 360

    # ---------------------
    # Animation methods
    # ---------------------
        
    def set_anim_name(self, name: str):
        if name != self.base_name:
            # Load new animation data from ResourceManager
            anim = self._rm.get_animationdata_reference(name)
            self.frames = anim.frames
            self.frame_durations = anim.durations
            self.tags = anim.tags
            self.final_offsets = anim.final_offsets
            self.sprite_size = anim.sprite_size
            self.base_name = name
            self.current_tag = None
            self.current_frame_idx = 0
            self.timer = 0
            self.playing = True
            self.png = anim.png
        
    def set_frame_tag(self, tag_name: str):
        """Set animation to specific tag."""
        if tag_name in self.tags:
            tag_data = self.tags[tag_name]
            self.current_tag = tag_name
            self.current_frame_idx = tag_data["from"]
            self.timer = 0
            self.playing = True

    def set_frame(self, frame_index: int):
        """Set animation to specific frame."""
        if 0 <= frame_index < len(self.frames):
            self.current_tag = None
            self.current_frame_idx = frame_index
            self.timer = 0
            self.playing = False

    # ---------------------
    # Update / Draw
    # ---------------------
    def update(self, dt: int):
        """Update current animation frame."""
        if not self.playing or not self.frames or self.png:
            return

        self.timer += dt
        current_frame_duration = self.frame_durations.get(self.current_frame_idx, 100)  # default to 100ms if not specified

        while self.timer >= current_frame_duration:
            self.timer -= current_frame_duration
            self.current_frame_idx += 1

            # Check for tag boundaries
            if self.current_tag:
                tag_data = self.tags[self.current_tag]
                if self.current_frame_idx > tag_data["to"]:
                    self.current_frame_idx = tag_data["from"]
            else:
                # Loop back to start if we exceed available frames
                if self.current_frame_idx >= len(self.frames):
                    self.current_frame_idx = 0

            current_frame_duration = self.frame_durations.get(self.current_frame_idx, 100)

    def draw(self, surface: pygame.Surface, world_pos: pygame.Vector2 | tuple[int, int]):

        if self.sprite_size == (0,0):
            return
        
        world_pos = world_pos + pygame.Vector2(self.final_offsets.get(self.current_frame_idx, (0, 0)))
        
        frame = None
        if self._rotation == 0 and not self._flip_x and not self._flip_y:
            #no rotation or flip, use original frame
            frame = self.frames[self.current_frame_idx]
        else:
            frame = self._get_transformed_frame()

        if frame:
            surface.blit(frame, world_pos)

    # ---------------------
    # Debug Draw
    # ---------------------

    def debug_draw(self, surface: pygame.Surface, world_pos: pygame.Vector2 | tuple[int, int]):
        pass

    # ---------------------
    # Private helpers
    # ---------------------
    def _get_transformed_frame(self) -> pygame.Surface | None:
        """Get current animation frame with rotation/flip applied, using ResourceManager cache."""

        # Determine angle to snap for caching
        self._snapped_rotation = round(self._rotation / 45) * 45 % 360

        # Use ResourceManager cached rotated+flipped frame
        return self._rm.get_rotated_frame(
            anim_name=self.base_name,
            frame_idx=self.current_frame_idx,
            angle=self._snapped_rotation,
            flip_x=self._flip_x,
            flip_y=self._flip_y
        )


