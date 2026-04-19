import pygame
from enum import Enum
from dataclasses import dataclass
import globals  
from debug_manager import DebugManager
from gameobjects.sprite import Sprite, RenderAnchor
from view_manager import ViewManager

class HitboxType(Enum):
    HIGH = "high"
    LOW = "low"

class HurtboxType(Enum):
    PUNCH = "punch"
    KICK = "kick"

@dataclass
class HitboxData:
    """Represents a hitbox with activation conditions."""
    rect: pygame.Rect
    hitbox_type: HitboxType
    base_name: str = None  # Must match animation base_name
    tag_name: str = None   # Must match current_tag["name"]
    frame: int = None      # Must match current_frame_idx
    
    def is_active(self, current_base_name: str, current_tag_name: str, current_frame: int) -> bool:
        """Check if this hitbox is active based on current animation state."""
        # base_name must always match if specified
        if self.base_name and self.base_name != current_base_name:
            return False
        
        # If frame is specified, it must match exactly
        if self.frame is not None:
            return self.frame == current_frame
        
        # If tag_name is specified, it must match
        if self.tag_name and self.tag_name != current_tag_name:
            return False
        
        # If only base_name is specified (or nothing), it's active
        return True

@dataclass
class HurtboxData:
    """Represents a hurtbox with activation conditions."""
    rect: pygame.Rect
    hurtbox_type: HurtboxType
    base_name: str = None  # Must match animation base_name
    tag_name: str = None   # Must match current_tag["name"]
    frame: int = None      # Must match current_frame_idx
    
    def is_active(self, current_base_name: str, current_tag_name: str, current_frame: int) -> bool:
        """Check if this hurtbox is active based on current animation state."""
        # base_name must always match if specified
        if self.base_name and self.base_name != current_base_name:
            return False
        
        # If frame is specified, it must match exactly
        if self.frame is not None:
            return self.frame == current_frame
        
        # If tag_name is specified, it must match
        if self.tag_name and self.tag_name != current_tag_name:
            return False
        
        # If only base_name is specified (or nothing), it's active
        return True

class GameObject():
    def __init__(self, pos, render_anchor: RenderAnchor = RenderAnchor.CENTER):

        self.anchor = render_anchor # this only affects drawingposition, hitbox/hurtbox positions are still relative to self.pos regardless of this setting. This is just for convenience when drawing sprites that are designed with center-bottom origin in mind.
        
        # World transform only
        self.screen_pos = pygame.Vector2(pos)
        self.world_pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)

        # Components
        self.sprites = []   # list of Sprite instances
        self.physics = None       # PhysicsComponent

        # Collision
        self.hurtbox: pygame.Rect = None
        self.hitbox: pygame.Rect = None

        # State
        self.active = True
        self.visible = True
        self.on_ground = None # update this from physics component to track if on ground for jump logic, etc.
       
        # ---------------------
        # Private attributes
        # ---------------------
        self._dm = DebugManager()
        self._vm = ViewManager()
        self._camera = None


    # ------------------------
    # Components
    # ------------------------
    def add_sprite(self, sprite, offset=(0, 0)):
        """Attach sprite as a visual child."""
        sprite.offset = pygame.Vector2(offset)
        self.sprites.append(sprite)
        return self

    def add_physics(self, physics_component):
        self.physics = physics_component
        physics_component.owner = self
        return self

    def add_camera(self, camera):
        self._camera = camera
        return self

    # ------------------------
    # Collision / Hurtbox
    # ------------------------
    def set_hurtbox(self, rect: pygame.Rect, relative_to_pos: bool = True):
        """Set hurtbox rectangle."""
        self.hurtbox = self._store_relative_rect(rect, relative_to_pos)

    def set_hitbox(self, rect: pygame.Rect, relative_to_pos: bool = True):
        """Set hitbox rectangle."""
        self.hitbox = self._store_relative_rect(rect, relative_to_pos)

    def _store_relative_rect(self, rect: pygame.Rect, relative_to_pos: bool) -> pygame.Rect:
        """Store rect relative to GameObject position."""
        if relative_to_pos:
            return rect.copy()
        return rect.move(-int(self.screen_pos.x), -int(self.screen_pos.y))

    def get_world_hurtbox(self) -> pygame.Rect | None:
        if self.hurtbox:
            return self.hurtbox.move(self.screen_pos)
        return None

    def get_world_hitbox(self) -> pygame.Rect | None:
        if self.hitbox:
            return self.hitbox.move(self.screen_pos)
        return None


    # ------------------------
    # Update
    # ------------------------
    def update(self, dt):
        if not self.active:
            return
        
        if self._camera:
            self.world_pos = self.screen_pos + (self._camera.x, self._camera.y)

        # Physics movement
        if self.physics:
            self.physics.update(dt)
            self.on_ground = self.physics.on_ground  # Update on_ground state from physics component


        # Sprite animation updates
        for sprite in self.sprites:
            sprite.update(dt)


        #print(f"GameObject at {self.screen_pos} and world pos {self.world_pos} with velocity {self.vel}, camera pos is ({self._camera.x}, {self._camera.y}))")


    # ------------------------
    # Draw
    # ------------------------
    def draw(self, surface):
        if not self.visible or not self.active:
            return
        
        # --- Draw sprites ---         
        for sprite in self.sprites:
            sprite.draw(surface, self.screen_pos, self.anchor, None)
        # --- End draw sprites ---



    # ------------------------
    # Debug drawing
    # ------------------------
    def debug_draw(self, surface: pygame.Surface):
        """ Draw world position point """
        self._dm.draw_circle_game(self.screen_pos.x, self.screen_pos.y, 0.5, globals.COLOR_YELLOW)


        """Draw sprite debug info."""
        for sprite in self.sprites:
            sprite.debug_draw(surface, self.screen_pos, self.anchor, None, debug_draw_text=False) 

        """Draw hurtbox / hitbox for debugging."""
        hitboxes = self.get_active_hitboxes()
        for rect, hitbox_type in hitboxes:
            self._dm.draw_rect_game(rect.topleft, rect.width, rect.height, globals.COLOR_RED)
      
        



    def add_hitbox(self, rect: pygame.Rect, hitbox_type: HitboxType, 
               base_name: str = None, tag_name: str = None, frame: int = None,
               relative_to_pos: bool = True):
        """Add a hitbox with metadata for frame-specific activation."""
        if not hasattr(self, 'hitboxes'):
            self.hitboxes = []
        
        stored_rect = self._store_relative_rect(rect, relative_to_pos)
        hitbox = HitboxData(stored_rect, hitbox_type, base_name, tag_name, frame)
        self.hitboxes.append(hitbox)


    def add_hurtbox(self, rect: pygame.Rect, hurtbox_type: HurtboxType,
                    base_name: str = None, tag_name: str = None, frame: int = None,
                    relative_to_pos: bool = True):
        """Add a hurtbox with metadata for frame-specific activation."""
        if not hasattr(self, 'hurtboxes'):
            self.hurtboxes = []
        
        stored_rect = self._store_relative_rect(rect, relative_to_pos)
        hurtbox = HurtboxData(stored_rect, hurtbox_type, base_name, tag_name, frame)
        self.hurtboxes.append(hurtbox)


    def get_active_hitboxes(self) -> list[tuple[pygame.Rect, HitboxType]]:
        """Get all currently active hitboxes based on sprite animation state."""
        if not hasattr(self, 'hitboxes') or not self.sprites:
            return []
        
        active = []
        
        # Get animation state from first sprite (or iterate all sprites if needed)
        sprite = self.sprites[0]
        if sprite._current_anim:
            anim = sprite._current_anim
            base_name = getattr(anim, 'base_name', None)
            tag_name = anim.current_tag['name'] if anim.current_tag else None
            frame_idx = anim.current_frame_idx
            
            for hitbox in self.hitboxes:
                if hitbox.is_active(base_name, tag_name, frame_idx):
                    world_rect = hitbox.rect.move(self.screen_pos)
                    active.append((world_rect, hitbox.hitbox_type))
        
        return active


    def get_active_hurtboxes(self) -> list[tuple[pygame.Rect, HurtboxType]]:
        """Get all currently active hurtboxes based on sprite animation state."""
        if not hasattr(self, 'hurtboxes') or not self.sprites:
            return []
        
        active = []
        
        # Get animation state from first sprite (or iterate all sprites if needed)
        sprite = self.sprites[0]
        if sprite._current_anim:
            anim = sprite._current_anim
            base_name = getattr(anim, 'base_name', None)
            tag_name = anim.current_tag['name'] if anim.current_tag else None
            frame_idx = anim.current_frame_idx
            
            for hurtbox in self.hurtboxes:
                if hurtbox.is_active(base_name, tag_name, frame_idx):
                    world_rect = hurtbox.rect.move(self.screen_pos)
                    active.append((world_rect, hurtbox.hurtbox_type))
        
        return active


   
