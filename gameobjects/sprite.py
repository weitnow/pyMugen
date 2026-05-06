import pygame
import managers.view_manager.camera as camera
from managers.graphic_manager import GraphicManager
from managers.debug_manager import DebugManager
from enum import Enum, auto

from managers.view_manager.view_manager import ViewManager

class RenderAnchor(Enum):
    CENTER = auto()
    TOPLEFT = auto()
    BOTTOMCENTER = auto()

class Sprite:
    def __init__(self, scale: int = 1):
        #PUBLIC attributes
        self.scale = scale

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
        self.active = False # wheter or not sprite gets updated/animated
        self.visible = True # wheter or not sprite gets drawn
        self.png = None # True if this sprite is a single PNG, False if it is an animation

        # Animation data - readonly (references to ResourceManager data, do NOT modify these!)
        self.frames = None  # is a Dict[int, pygame.Surface], reference, do NOT modify!
        self.frame_durations = None  # is a Dict[int, int] mapping frame index to duration in ms, reference, do NOT modify!
        self.tags = None  # is a Dict[str, Dict[str, int]] mapping tag name to {"from": int, "to": int}, reference, do NOT modify!
        self.final_offsets = None  # is a Dict[int, (x, y)], reference, do NOT modify!

        # Private attributes
        self._gm: GraphicManager = GraphicManager()
        self._dm: DebugManager = DebugManager()
        self._vm: ViewManager = ViewManager()
        self._draw_surface = self._vm.game_surface # surface to draw on, usually the main game surface but can be changed for special effects, etc
        self._camera = self._vm.camera # dont modify camera directly from sprite, it should be handled by the view manager, this is just a reference for convenience when drawing
        self._use_camera = True # whether to apply camera transformations when drawing this sprite, can be toggled for testing/debugging purposes
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
            anim = self._gm.get_animationdata_reference(name, self.scale)
            self.frames = anim.frames
            self.frame_durations = anim.durations
            self.tags = anim.tags
            self.final_offsets = anim.final_offsets
            self.sprite_size = anim.sprite_size
            self.base_name = name
            self.current_tag = None
            self.current_frame_idx = 0
            self.timer = 0
            self.active = True
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
            self.active = True
        return self

    def set_frame(self, frame_index: int):
        """Set animation to specific frame."""
        if 0 <= frame_index < len(self.frames):
            self.current_tag = None
            self.current_frame_idx = frame_index
            self.timer = 0
            self.active = False
        return self
    
    def use_camera(self, use: bool): #TODO at scrollfactor speed
        """Set whether to apply camera transformations when drawing this sprite."""
        self._use_camera = bool(use)
        return self
    

    def set_scale(self, scale: int):
        """
        Switch to a different scale of the current animation.
        If the scaled variant doesn't exist in GraphicManager yet, it is created
        automatically from the scale=1 source. Preserves the current tag.
        """
        if self.base_name is None and not self.png:
            raise RuntimeError("No animation loaded. Call set_anim_name() first.")
        if scale < 1:
            raise ValueError(f"Scale factor must be >= 1, got {scale}.")
        if scale == self.scale:
            return self  # nothing to do

        # Create the scaled variant if it doesn't exist yet
        self._gm.get_or_create_scaled(self.base_name, scale)

        # Switch scale and re-point all references
        saved_tag = self.current_tag
        self.scale = scale

        anim = self._gm.get_animationdata_reference(self.base_name, self.scale)
        self.frames = anim.frames
        self.frame_durations = anim.durations
        self.tags = anim.tags
        self.final_offsets = anim.final_offsets
        self.sprite_size = anim.sprite_size
        self.png = anim.png
        self._current_offset = self.final_offsets.get(self.current_frame_idx, (0, 0))

        # Restore tag if it still exists
        if saved_tag and saved_tag in self.tags:
            self.set_frame_tag(saved_tag)

        return self  # allow chaining

    # ---------------------
    # Update / Draw
    # ---------------------
    def update(self, dt: float):
        """Update current animation frame."""
        if not self.active or not self.frames or self.png:
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

    def draw(self, world_pos, render_anchor: RenderAnchor = RenderAnchor.CENTER):

        # if there are no frames or sprite size is (0,0), skip drawing to avoid errors
        if not self.frames or self.sprite_size == (0, 0) or not self.visible:
            return

        x, y = world_pos

        # --- Camera ---
        if self._use_camera: # move x/y according to camera
            x -= self._camera.x
            y -= self._camera.y

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

        

        # --- Get frame ---
        if self._rotation == 0 and not self._flip_x and not self._flip_y:
            frame = self.frames[self.current_frame_idx]
        else:
            # get transformed frame from ResourceManager cache (handles rotation and flipping)
            frame = self._get_transformed_frame()

        self._draw_rect.size = frame.get_size()
        self._draw_rect.center = (x, y)

        self._draw_surface.blit(frame, self._draw_rect)


    # ---------------------
    # Debug Draw
    # ---------------------

    def debug_draw(self, world_pos: pygame.Vector2, render_anchor: RenderAnchor = RenderAnchor.CENTER): #TODO: implement camera support
     
        x, y = world_pos

        if self._use_camera:
            x -= self._camera.x
            y -= self._camera.y

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
            world_pos[0] - 2 - self._camera.x if self._use_camera else world_pos[0] - 2,
            world_pos[1] - 2 - self._camera.y if self._use_camera else world_pos[1] - 2,
            width=4,
            height=4,
            color=(255, 0, 255)

        )


        # Draw text with world position and current tag for debugging
        if self._dm.debug_text:
            self._dm.draw_debug_text(x + offset_x - self.sprite_size[0] // 2, y + offset_y - self.sprite_size[1] // 2 - 10, text=f"world_pos: {world_pos}, screen_pos: ({world_pos[0] - self._camera.x if self._use_camera else world_pos[0]}, {world_pos[1] - self._camera.y if self._use_camera else world_pos[1]}), cam_pos: ({self._camera.x}, {self._camera.y})", color=(247, 0, 255))
    
                                


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
            flip_y=self._flip_y,
            scale=self.scale
        )


