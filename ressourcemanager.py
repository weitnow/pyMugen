import json
import pygame
from typing import Dict
from animationdata import AnimationData

class ResourceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance.animations = {}
        return cls._instance

    def load_spritesheet(self, name: str, image_path: str, json_path: str):
        if name in self.animations:
            return

        with open(json_path, "r") as f:
            data = json.load(f)

        spritesheet = pygame.image.load(image_path).convert_alpha()

        frames = {}
        durations = {}
        for k, v in data["frames"].items():
            idx = int(k)
            rect = pygame.Rect(v["frame"]["x"], v["frame"]["y"], v["frame"]["w"], v["frame"]["h"])
            frames[idx] = spritesheet.subsurface(rect).copy()
            durations[idx] = v.get("duration", 100)

        tags = data.get("meta", {}).get("frameTags", [])

        # store base data (shared)
        self.animations[name] = {
            "spritesheet": spritesheet,
            "frames": frames,
            "durations": durations,
            "tags": tags
        }

    def get_animation_instance(self, name: str) -> AnimationData:
        """Returns a fresh AnimationData instance (unique state)"""
        base = self.animations[name]
        return AnimationData(
            base["spritesheet"],
            base["frames"],
            base["durations"],
            base["tags"]
        )
