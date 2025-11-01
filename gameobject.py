import pygame
from ressourcemanager import ResourceManager

class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.animations = {}
        self.current_anim = None
        self.image = None
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

    def get_anim(self, name: str):
        """Requests a new AnimationData instance from ResourceManager"""
        rm = ResourceManager()
        anim = rm.get_animation_instance(name)
        self.animations[name] = anim
        return anim

    def set_anim(self, name: str):
        if name in self.animations:
            self.current_anim = self.animations[name]
        else:
            print(f"Animation '{name}' not found for this object")

    def set_frame_tag(self, tag_name: str):
        if self.current_anim:
            self.current_anim.set_tag(tag_name)

    def update(self, dt):
        if self.current_anim:
            self.current_anim.update(dt)
            self.image = self.current_anim.get_current_frame()
            self.rect.size = self.image.get_size()

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
