import pygame
from ressourcemanager import ResourceManager
from animationdata import AnimationData

class GameObject:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.animations: dict[str, AnimationData] = {}
        self.current_anim: AnimationData | None = None
        self.visible = True

    # --- load animation instance from ResourceManager ---
    def get_anim(self, name: str):
        rm = ResourceManager()
        if name not in self.animations:
            self.animations[name] = rm.get_animation_instance(name)

    # --- select active animation ---
    def set_anim(self, name: str):
        if name in self.animations:
            self.current_anim = self.animations[name]

    # --- set tag-based animation (for spritesheets with frameTags) ---
    def set_frame_tag(self, tag_name: str):
        if self.current_anim:
            self.current_anim.set_tag(tag_name)

    # --- set a specific frame (for spritesheets without tags or static images) ---
    def set_frame(self, frame_index: int):
        if self.current_anim:
            self.current_anim.set_frame(frame_index)

    # --- update animation timer ---
    def update(self, dt: int):
        if self.current_anim:
            self.current_anim.update(dt)

    # --- draw current frame ---
    def draw(self, surface: pygame.Surface):
        if not self.visible or not self.current_anim:
            return
        frame = self.current_anim.get_current_frame()
        surface.blit(frame, self.pos)
