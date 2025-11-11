import json
import pygame
from typing import Dict, List

class AnimationData:
    def __init__(self, frames: Dict[int, pygame.Surface], durations: Dict[int, int] = None, tags: List[dict] = None):
        self.frames = frames                     # int -> Surface
        self.durations = durations or {i: 100 for i in frames}   # fallback 100ms
        self.tags = tags or []                   # list of {"name": str, "from": int, "to": int}

        self.current_tag = None
        self.current_frame_idx = 0
        self.timer = 0
        self.playing = False

    # --- TAG-BASED ANIMATION ---
    def set_tag(self, tag_name: str):
        for tag in self.tags:
            if tag["name"] == tag_name:
                self.current_tag = tag
                self.current_frame_idx = tag["from"]
                self.timer = 0
                self.playing = True
                return

    # --- FRAME-BASED ANIMATION (for spritesheets without tags) ---
    def set_frame(self, frame_idx: int):
        if frame_idx not in self.frames:
            raise ValueError(f"Frame index {frame_idx} not in animation frames.")
        
        self.current_frame_idx = frame_idx
        self.current_tag = None
        self.timer = 0
        self.playing = False

            

    def update(self, dt: int):
        if self.current_tag and self.playing:
            self.timer += dt
            idx = self.current_frame_idx
            if self.timer >= self.durations[idx]:
                self.timer -= self.durations[idx]
                self.current_frame_idx += 1
                if self.current_frame_idx > self.current_tag["to"]:
                    self.current_frame_idx = self.current_tag["from"]

    def get_current_frame(self) -> pygame.Surface:
        return self.frames[self.current_frame_idx]
    

class ResourceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance.animations = {}
            # shared cache for rotated/flipped frames across all gameobjects
            cls._instance._rotation_cache = {}
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
            durations[idx] = v.get("duration", 100)  # default 100ms TODO: make this configurable

        tags = data.get("meta", {}).get("frameTags", [])

        # store base data (shared)
        self.animations[name] = {
            "frames": frames,
            "durations": durations,
            "tags": tags
        }

     # --- SINGLE PNG ---
    def load_png(self, name: str, image_path: str):
        if name in self.animations:
            return

        image = pygame.image.load(image_path).convert_alpha()
        self.animations[name] = {
            "frames": {0: image},
            "durations": {0: 0},
            "tags": []
        }

    def get_animation_instance(self, name: str) -> AnimationData:
        """Returns a fresh AnimationData instance (unique state)"""
        base = self.animations[name]
        anim = AnimationData(
            base["frames"],
            base["durations"],
            base["tags"]
        )
        # attach base name so callers can request shared rotated frames
        anim.base_name = name
        return anim

    def get_rotated_frame(self, anim_name: str, frame_idx: int, angle: int, flip_x: bool = False, flip_y: bool = False) -> pygame.Surface:
        """Return a rotated+flipped Surface for a given animation frame.

        This uses a shared cache so rotation is computed at most once per
        (animation, frame_idx, angle, flip_x, flip_y) combination.
        """
        key = (anim_name, frame_idx, angle % 360, bool(flip_x), bool(flip_y))
        cache = self._rotation_cache
        if key in cache:
            return cache[key]

        base = self.animations[anim_name]
        frame = base["frames"][frame_idx]
        rotated = pygame.transform.rotate(frame, angle)
        if flip_x or flip_y:
            rotated = pygame.transform.flip(rotated, flip_x, flip_y)

        cache[key] = rotated
        return rotated