import pygame
from graphic_manager import GraphicManager
from debug_manager import DebugManager
from enum import Enum, auto

class RenderAnchor(Enum):
    CENTER = auto()
    TOPLEFT = auto()
    BOTTOMMID = auto()

class Sprite:
    def __init__(self):
        # PUBLIC attributes (with property access)
        self._flip_x: bool = False
        self._flip_y: bool = False
        self._rotation: int = 0     
        
        # Animation data
        self.frames = None  # is a Dict[int, pygame.Surface], reference, do NOT modify!
        self.frame_durations = None  # is a Dict[int, int] mapping frame index to duration in ms, reference, do NOT modify!
        self.tags = None  # is a Dict[str, Dict[str, int]] mapping tag name to {"from": int, "to": int}, reference, do NOT modify!
        self.final_offsets = None  # is a Dict[int, (x, y)], reference, do NOT modify!
        self.sprite_size = (0,0)  # is a tuple (width, height) 
       
        self.base_name = None # is a str name of the current animation-file
        self.current_tag = None # is a str name of the current tag
        self.current_frame_idx = 0
        self.timer = 0
        self.playing = False
        self.png = False # True if this sprite is a single PNG, False if it is an animation
        
        # Private attributes
        self._rm: GraphicManager = GraphicManager()
        self._dm: DebugManager = DebugManager()
        self._snapped_rotation: int = 0
        self._rect = None # pygame.rect set later
        
        
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
        return self # allow chaining
        
    def set_frame_tag(self, tag_name: str):
        """Set animation to specific tag."""
        if tag_name == self.current_tag:
            return self # no change

        if tag_name in self.tags:
            tag_data = self.tags[tag_name]
            self.current_tag = tag_name
            self.current_frame_idx = tag_data["from"]
            self.timer = 0
            self.playing = True
        return self

    def set_frame(self, frame_index: int):
        """Set animation to specific frame."""
        if 0 <= frame_index < len(self.frames):
            self.current_tag = None
            self.current_frame_idx = frame_index
            self.timer = 0
            self.playing = False
        return self

    # ---------------------
    # Update / Draw
    # ---------------------
    def update(self, dt: float):
        """Update current animation frame."""
        if not self.playing or not self.frames or self.png:
            return

        self.timer += dt * 1000.0  # Convert dt to milliseconds
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

    def draw(self, surface: pygame.Surface, world_pos, render_anchor: RenderAnchor = RenderAnchor.CENTER, camera=None):

        if not self.frames or self.sprite_size == (0, 0):
            return

        # --- Use raw numbers instead of Vector2 (PERF FIX #1) ---
        x, y = world_pos

        # --- Anchor adjustment ---
        if render_anchor == RenderAnchor.TOPLEFT:
            x += self.sprite_size[0] // 2
            y += self.sprite_size[1] // 2
        elif render_anchor == RenderAnchor.BOTTOMMID:
            y += self.sprite_size[1] // 2

        # --- Offset lookup ---
        offset_x, offset_y = self.final_offsets.get(self.current_frame_idx, (0, 0))

        if self._flip_x:
            offset_x = -offset_x
        if self._flip_y:
            offset_y = -offset_y

        x += offset_x
        y += offset_y

        # --- Camera (PERF FIX #3) ---
        if camera:
            # assume camera has x/y instead of returning Vector2
            x -= camera.x
            y -= camera.y

        # --- Get frame ---
        if self._rotation == 0 and not self._flip_x and not self._flip_y:
            frame = self.frames[self.current_frame_idx]
        else:
            frame = self._get_transformed_frame()

        # --- Reuse rect (PERF FIX #2) ---
        if self._rect is None:
            self._rect = pygame.Rect(0, 0, 0, 0)

        self._rect.size = frame.get_size()
        self._rect.center = (x, y)

        surface.blit(frame, self._rect)




    # ---------------------
    # Debug Draw
    # ---------------------

    def debug_draw(self, surface: pygame.Surface, world_pos: pygame.Vector2, render_anchor: RenderAnchor = RenderAnchor.CENTER, camera=None): #TODO: implement camera support
        # Original sprite rectangle (dark grey) 

        world_pos = pygame.Vector2(world_pos)  # make a copy to avoid modifying caller's vector
        if render_anchor == RenderAnchor.CENTER:
            pass  # default is already center
        elif render_anchor == RenderAnchor.TOPLEFT:
            world_pos += pygame.Vector2(self.sprite_size[0] // 2, self.sprite_size[1] // 2)
        elif render_anchor == RenderAnchor.BOTTOMMID:
            world_pos += pygame.Vector2(0, self.sprite_size[1] // 2)

        # offset could be an empty dict if no offsets were defined for this animation, so default to (0,0)
        offset_x, offset_y = self.final_offsets.get(self.current_frame_idx, (0, 0))
        
        # Draw the original sprite rect (with offset) in dark grey for debugging
        self._dm.draw_rect_game(
            pos=(world_pos[0] + offset_x - self.sprite_size[0] // 2, world_pos[1] + offset_y - self.sprite_size[1] // 2),
            width=self.sprite_size[0],
            height=self.sprite_size[1],
            color=(150, 150, 150)
            )
        
        # Draw a small cross in the center of the sprite which is also the rotation point
        self._dm.draw_crossed_rect_game(pos=world_pos - pygame.Vector2(2, 2), width=4, height=4, color=(150, 150, 150))

        self._dm.draw_text_game(pos=(world_pos[0] + 4, world_pos[1]), text=f"Pos: {world_pos} Tag: {self.current_tag}", color=(150, 150, 150))
   
                                


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


