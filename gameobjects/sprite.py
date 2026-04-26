import pygame
import camera
from graphic_manager import GraphicManager
from debug_manager import DebugManager
from enum import Enum, auto

from view_manager import ViewManager

class RenderAnchor(Enum):
    CENTER = auto()
    TOPLEFT = auto()
    BOTTOMCENTER = auto()

class Sprite:
    def __init__(self):
        # PUBLIC attributes (with property access)
        self._flip_x: bool = False
        self._flip_y: bool = False
        self._rotation: int = 0     

        # Animation data        
        self.sprite_size = (0,0)  # is a tuple (width, height) 
        self.base_name = None # is a str name of the current animation-file
        self.current_tag = None # is a str name of the current tag
        self.current_frame_idx = 0 # is an int index of the current frame within the animation for this sprite
        self.timer = 0
        self.playing = False
        self.png = False # True if this sprite is a single PNG, False if it is an animation

        # Animation data - readonly (references to ResourceManager data, do NOT modify these!)
        self.frames = None  # is a Dict[int, pygame.Surface], reference, do NOT modify!
        self.frame_durations = None  # is a Dict[int, int] mapping frame index to duration in ms, reference, do NOT modify!
        self.tags = None  # is a Dict[str, Dict[str, int]] mapping tag name to {"from": int, "to": int}, reference, do NOT modify!
        self.final_offsets = None  # is a Dict[int, (x, y)], reference, do NOT modify!
        
        # Private attributes
        self._gm: GraphicManager = GraphicManager()
        self._dm: DebugManager = DebugManager()
        self._vm: ViewManager = ViewManager()
        self._snapped_rotation: int = 0
        self._current_offset = (0, 0) # current frame offset, updated in update() if frame changes
        self._draw_rect = pygame.Rect(0, 0, 0, 0)
        
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
        self._snapped_rotation = round(self._rotation / 45) * 45 % 360  # update snapped rotation for caching

    # ---------------------
    # Animation methods
    # ---------------------
        
    def set_anim_name(self, name: str):
        if name != self.base_name:
            # Load new animation data from ResourceManager
            anim = self._gm.get_animationdata_reference(name)
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
            self._current_offset = self.final_offsets.get(0, (0, 0)) #get offset for first frame, if there is none get (0,0)
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

            # Update current offset property for the current frame, if there is none default to (0,0)        
            self._current_offset = self.final_offsets.get(self.current_frame_idx, (0, 0))

            # Update current frame duration for the current frame, if there is none default to 100ms
            current_frame_duration = self.frame_durations.get(self.current_frame_idx, 100)

    def draw(self, surface: pygame.Surface, world_pos, render_anchor: RenderAnchor = RenderAnchor.CENTER, camera=None):

        # if there are no frames or sprite size is (0,0), skip drawing to avoid errors
        if not self.frames or self.sprite_size == (0, 0):
            return

        x, y = world_pos

        # --- Anchor adjustment ---
        if render_anchor == RenderAnchor.TOPLEFT:
            x += self.sprite_size[0] // 2
            y += self.sprite_size[1] // 2
        elif render_anchor == RenderAnchor.BOTTOMCENTER:
            y -= self.sprite_size[1] // 2

        # --- Offset lookup ---
        offset_x, offset_y = self._current_offset

        if self._flip_x:
            offset_x = -offset_x
        if self._flip_y:
            offset_y = -offset_y

        # Apply offsets to position
        x += offset_x
        y += offset_y

        # --- Camera ---
        if camera: # move x/y according to camera
            x -= camera.x
            y -= camera.y

        # --- Get frame ---
        if self._rotation == 0 and not self._flip_x and not self._flip_y:
            frame = self.frames[self.current_frame_idx]
        else:
            # get transformed frame from ResourceManager cache (handles rotation and flipping)
            frame = self._get_transformed_frame()

        self._draw_rect.size = frame.get_size()
        self._draw_rect.center = (x, y)

        surface.blit(frame, self._draw_rect)


    # ---------------------
    # Debug Draw
    # ---------------------

    def debug_draw(self, surface: pygame.Surface, world_pos: pygame.Vector2, render_anchor: RenderAnchor = RenderAnchor.CENTER, camera=None): #TODO: implement camera support
     
        x, y = world_pos

        # --- Anchor adjustment --- but only if sprite size is not (0,0) to avoid weird anchor behavior when there is no sprite loaded yet
        if self.sprite_size != (0, 0):
            if render_anchor == RenderAnchor.TOPLEFT:
                x += self.sprite_size[0] // 2
                y += self.sprite_size[1] // 2
            elif render_anchor == RenderAnchor.BOTTOMCENTER:
                y -= self.sprite_size[1] // 2

        # starting here x and y are the world position of the sprite with anchor adjustment, but before offset and camera

        # --- Offset lookup ---
        offset_x, offset_y = self._current_offset

        cam_x = camera.x if camera else 0
        cam_y = camera.y if camera else 0

        x -= cam_x
        y -= cam_y

        if self._flip_x:
            offset_x = -offset_x
        if self._flip_y:
            offset_y = -offset_y

        # Draw the original sprite rect (with offset) for debugging
        self._vm.draw_rect_outline(
            x + offset_x - self.sprite_size[0] // 2,
            y + offset_y - self.sprite_size[1] // 2,
            width=self.sprite_size[0],
            height=self.sprite_size[1],
            color=(247, 0, 255)
            )

        # Draw a small circle in the center of the sprite which is also the rotation point
        self._vm.draw_circle(x + offset_x, y + offset_y, radius=4, color=(255, 255, 0))

        #Draw a small rectangle at the origin point
        self._vm.draw_rect(
            world_pos[0] - 2 - cam_x,
            world_pos[1] - 2 - cam_y,
            width=4,
            height=4,
            color=(255, 0, 255)

        )


        # Draw text with world position and current tag for debugging
        self._dm.draw_debug_text(x + offset_x - self.sprite_size[0] // 2, y + offset_y - self.sprite_size[1] // 2 - 10, text=f"world_pos: {world_pos}, screen_pos: ({x + offset_x}, {y + offset_y}), Tag: {self.current_tag}", color=(247, 0, 255))
    
                                


    # ---------------------
    # Private helpers
    # ---------------------
    def _get_transformed_frame(self) -> pygame.Surface | None:
        """Get current animation frame with rotation/flip applied, using ResourceManager cache."""


        # Use ResourceManager cached rotated+flipped frame
        return self._gm.get_rotated_frame(
            anim_name=self.base_name,
            frame_idx=self.current_frame_idx,
            angle=self._snapped_rotation,
            flip_x=self._flip_x,
            flip_y=self._flip_y
        )


