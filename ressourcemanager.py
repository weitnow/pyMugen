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

        spritesheet = pygame.image.load(image_path).convert_alpha()
        frames = {}
        frames_data = data["frames"]

        # Sort by frame index so animation order is correct
        sorted_keys = sorted(frames_data.keys(), key=lambda k: int(k.split()[1].split(".")[0]))

        for key in sorted_keys:
            frame_info = frames_data[key]["frame"]
            rect = pygame.Rect(frame_info["x"], frame_info["y"], frame_info["w"], frame_info["h"])
            frames[key] = spritesheet.subsurface(rect).copy()

        tags = data["meta"]["frameTags"]

        self.animations[name] = AnimationData(spritesheet, frames, tags)

    def get_animation_data(self, name: str) -> AnimationData:
        return self.animations[name] 
