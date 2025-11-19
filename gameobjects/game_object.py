import pygame
import globals  # for DEBUG_SCALE if you use debug drawing
from debug_manager import DebugManager

class GameObject:
    def __init__(self, pos=(0, 0)):
        # World transform only
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)

        # Components
        self.sprites = []         # list of Sprite instances
        self.physics = None       # PhysicsComponent

        # Collision
        self.hurtbox: pygame.Rect | None = None
        self.hitbox: pygame.Rect | None = None

        # State
        self.active = True
        self.visible = True

        # Debug
        self._debug_manager = DebugManager()


    # ------------------------
    # Components
    # ------------------------
    def add_sprite(self, sprite, offset=(0, 0)):
        """Attach sprite as a visual child."""
        sprite.offset = pygame.Vector2(offset)
        self.sprites.append(sprite)

    def set_physics(self, physics_component):
        self.physics = physics_component
        physics_component.owner = self


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
        return rect.move(-int(self.pos.x), -int(self.pos.y))

    def get_world_hurtbox(self) -> pygame.Rect | None:
        if self.hurtbox:
            return self.hurtbox.move(self.pos)
        return None

    def get_world_hitbox(self) -> pygame.Rect | None:
        if self.hitbox:
            return self.hitbox.move(self.pos)
        return None


    # ------------------------
    # Update
    # ------------------------
    def update(self, dt):
        if not self.active:
            return

        # Physics movement
        if self.physics:
            self.physics.update(dt)

        # Sprite animation updates
        for sprite in self.sprites:
            sprite.update(dt)


    # ------------------------
    # Draw
    # ------------------------
    def draw(self, surface):
        if not self.visible:
            return
            
        for sprite in self.sprites:
            world_pos = self.pos + sprite.offset
            sprite.draw(surface, world_pos)

        self.draw_debug(surface)


    # ------------------------
    # Debug drawing
    # ------------------------
    def draw_debug(self, surface: pygame.Surface):
        """Draw hurtbox / hitbox for debugging."""
        if not self._debug_manager.debug_on:
            return

        scale = globals.DEBUG_SCALE

        if self.hurtbox:
            pygame.draw.rect(surface, (0, 0, 255), self.get_world_hurtbox(), 1)

        if self.hitbox:
            pygame.draw.rect(surface, (255, 0, 0), self.get_world_hitbox(), 1)
