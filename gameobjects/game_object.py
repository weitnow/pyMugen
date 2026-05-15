import pygame
from enum import Enum
from dataclasses import dataclass
import globals
from gameobjects.sprite import Sprite, RenderAnchor


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
    base_name: str = None
    tag_name: str = None
    frame: int = None

    def is_active(self, current_base_name: str, current_tag_name: str, current_frame: int) -> bool:
        if self.base_name and self.base_name != current_base_name:
            return False
        if self.frame is not None:
            return self.frame == current_frame
        if self.tag_name and self.tag_name != current_tag_name:
            return False
        return True

@dataclass
class HurtboxData:
    """Represents a hurtbox with activation conditions."""
    rect: pygame.Rect
    hurtbox_type: HurtboxType
    base_name: str = None
    tag_name: str = None
    frame: int = None

    def is_active(self, current_base_name: str, current_tag_name: str, current_frame: int) -> bool:
        if self.base_name and self.base_name != current_base_name:
            return False
        if self.frame is not None:
            return self.frame == current_frame
        if self.tag_name and self.tag_name != current_tag_name:
            return False
        return True


class GameObject(Sprite):
    def __init__(self, world_pos, render_anchor: RenderAnchor = RenderAnchor.CENTER):
        super().__init__()

        self.anchor = render_anchor
        self.world_pos = pygame.Vector2(world_pos)
        self.on_ground = None
        self.vel = pygame.Vector2(0, 0)

        # Camera
        self._use_camera = False

        # Components
        self.physics = None

        # Collision
        self.hitboxes: list[HitboxData] = []
        self.hurtboxes: list[HurtboxData] = []

    # ------------------------
    # Components
    # ------------------------
    def add_physics(self, physics_component):
        self.physics = physics_component
        physics_component.owner = self
        return self

    def enable_camera(self):
        self._use_camera = True
        return self

    def disable_camera(self):
        self._use_camera = False
        return self

    # ------------------------
    # Update
    # ------------------------
    def update(self, dt):
        if not self.active:
            return

        if self.physics:
            self.physics.update(dt)
            self.on_ground = self.physics.on_ground

        super().update(dt)

    # ------------------------
    # Draw
    # ------------------------
    def draw(self):
        if not self.visible:
            return
        screen_pos = self._vm.camera.apply_vec2(self.world_pos) if self._use_camera else self.world_pos
        super().draw(screen_pos, self.anchor)

    # ------------------------
    # Debug drawing
    # ------------------------
    def debug_draw(self):
        screen_pos = self._vm.camera.apply_vec2(self.world_pos) if self._use_camera else self.world_pos
        super().debug_draw(screen_pos, self.anchor)

        for rect, _ in self.get_active_hitboxes():
            screen_rect = self._vm.camera.apply(rect) if self._use_camera else rect
            self._vm.draw_rect_outline(screen_rect.x, screen_rect.y, screen_rect.width, screen_rect.height, globals.COLOR_RED)

        for rect, _ in self.get_active_hurtboxes():
            screen_rect = self._vm.camera.apply(rect) if self._use_camera else rect
            self._vm.draw_rect_outline(screen_rect.x, screen_rect.y, screen_rect.width, screen_rect.height, globals.COLOR_GREEN)

    # ------------------------
    # Hitboxes / Hurtboxes
    # ------------------------
    def add_hitbox(self, rect: pygame.Rect, hitbox_type: HitboxType,
                   base_name: str = None, tag_name: str = None, frame: int = None):
        """Add a hitbox. rect is relative to world_pos."""
        self.hitboxes.append(HitboxData(rect.copy(), hitbox_type, base_name, tag_name, frame))

    def add_hurtbox(self, rect: pygame.Rect, hurtbox_type: HurtboxType,
                    base_name: str = None, tag_name: str = None, frame: int = None):
        """Add a hurtbox. rect is relative to world_pos."""
        self.hurtboxes.append(HurtboxData(rect.copy(), hurtbox_type, base_name, tag_name, frame))

    def get_active_hitboxes(self) -> list[tuple[pygame.Rect, HitboxType]]:
        """Get all active hitboxes in world space."""
        if not self.hitboxes:
            return []
        tag_name = self.current_tag["name"] if self.current_tag else None
        return [
            (hb.rect.move(self.world_pos), hb.hitbox_type)
            for hb in self.hitboxes
            if hb.is_active(self.base_name, tag_name, self.current_frame_idx)
        ]

    def get_active_hurtboxes(self) -> list[tuple[pygame.Rect, HurtboxType]]:
        """Get all active hurtboxes in world space."""
        if not self.hurtboxes:
            return []
        tag_name = self.current_tag["name"] if self.current_tag else None
        return [
            (hb.rect.move(self.world_pos), hb.hurtbox_type)
            for hb in self.hurtboxes
            if hb.is_active(self.base_name, tag_name, self.current_frame_idx)
        ]