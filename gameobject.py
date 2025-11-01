import pygame
from ressourcemanager import ResourceManager
from animationdata import AnimationData

class GameObject(pygame.sprite.Sprite):
    def __init__(self, resource_name: str, pos: pygame.Vector2):
        super().__init__()
        resources = ResourceManager()
        self.anim_data: AnimationData = resources.get_animation_data(resource_name)
      

        self.current_tag: str = self.anim_data.tags[0] # sets the first tag from the asepritefile as current_tag (for example "Idle")
        self.current_frame_index: int = self.current_tag["from"]
        self.current_direction = 1
        self.timer = 0

        # Prepare initial image and position
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        self.update_image()

    def set_frame_tag(self, tag_name: str):
        tag = next((t for t in self.anim_data.tags if t["name"] == tag_name), None)
        if not tag:
            raise ValueError(f"Tag '{tag_name}' not found")
        self.current_tag = tag
        self.current_frame_index = tag["from"]
        self.timer = 0
        self.update_image()

    def update_image(self):
        # frame_keys is an ordered list of integer frame indices; map current_frame_index to that key
        key = self.anim_data.frame_keys[self.current_frame_index]
        self.image = self.anim_data.frames[key]
        # update rect size to match the new image while preserving topleft position
        topleft = self.rect.topleft
        self.rect = self.image.get_rect(topleft=topleft)

    def update(self, dt: int):
        tag = self.current_tag
        start, end = tag["from"], tag["to"]
        direction_type = tag.get("direction", "forward")
        duration = 100  # fixed duration for now (can be improved) #TODO: get duration from frame data

        self.timer += dt
        while self.timer >= duration:
            self.timer -= duration
            if direction_type == "forward":
                self.current_frame_index = start if self.current_frame_index >= end else self.current_frame_index + 1
            elif direction_type == "reverse":
                self.current_frame_index = end if self.current_frame_index <= start else self.current_frame_index - 1
            elif direction_type == "pingpong":
                self.current_frame_index += self.current_direction
                if self.current_frame_index > end:
                    self.current_direction = -1
                    self.current_frame_index = end - 1
                elif self.current_frame_index < start:
                    self.current_direction = 1
                    self.current_frame_index = start + 1
            self.update_image()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
