import json
import pygame
from animationdata import AnimationData
from typing import Dict, Any

class ResourceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance.animations = {}
        return cls._instance

    def load_spritesheet(self, name: str, image_path: str, json_path: str):
        if name in self.animations:
            return  # already loaded

        with open(json_path, "r") as file:
            data = json.load(file)

        # spritesheet holds a pygame.Surface of the entire image  
        spritesheet = pygame.image.load(image_path).convert_alpha()

        # frames: int -> Surface ; durations: int -> duration (ms)
        frames: Dict[int, pygame.Surface] = {}
        durations: Dict[int, int] = {}
        for k, v in data["frames"].items():
            idx = int(k)
            rect = pygame.Rect(v["frame"]["x"], v["frame"]["y"], v["frame"]["w"], v["frame"]["h"])
            frames[idx] = spritesheet.subsurface(rect).copy()
            durations[idx] = v.get("duration", 100)

        # Handle tags only if present
        tags = data.get("meta", {}).get("frameTags", [])

        self.animations[name] = AnimationData(spritesheet, frames, tags, durations)


    def get_animation_data(self, name: str) -> AnimationData:
        return self.animations[name]


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    resources = ResourceManager()
    resources.load_spritesheet(
        "gbFighter",
        "Assets/Graphics/Aseprite/gbFighter.png",
        "Assets/Graphics/Aseprite/gbFighter.json"
    )


"""
    gbFighter, Idle, from, to, 

    gbFighter, 0, surface, duration
"""