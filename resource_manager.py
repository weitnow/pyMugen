import json
import pygame
from typing import Dict, List
from decorators import singleton

class AnimationData:
    def __init__(self, frames: Dict[int, pygame.Surface], durations: Dict[int, int] = None, tags: Dict[str, dict] = None, sprite_size: tuple = (0,0)):

        # self.frames is a dict mapping frame index to Surface
        self.frames = frames                # int -> Surface
        self.durations = durations              # int -> duration in ms
        self.tags = tags                       # list of {"name": str, "from": int, "to": int}
        self.sprite_size = sprite_size                   # (width, height)

        self.current_tag = None
        self.current_frame_idx = 0
        self.timer = 0
        self.playing = False

    # --- TAG-BASED ANIMATION ---
    def set_tag(self, tag_name):
        try:
            self.current_tag = self.tags[tag_name]
        except KeyError:
            return

        self.current_frame_idx = self.current_tag["from"]
        self.timer = 0
        self.playing = True


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
    


@singleton
class ResourceManager:
    def __init__(self):
        self.animations = {}
        self._rotation_cache = {}   # shared cache across all objects

    def load_spritesheet(self, name: str, image_path: str, json_path: str):
        if name in self.animations:
            raise ValueError(f"Spritesheet with name '{name}' already loaded.")

        with open(json_path, "r") as f:
            data = json.load(f)

        spritesheet = pygame.image.load(image_path).convert_alpha()

        frames = {}
        durations = {}

        for k, v in data["frames"].items():
            idx = int(k)
            rect = pygame.Rect(
                v["frame"]["x"],
                v["frame"]["y"],
                v["frame"]["w"],
                v["frame"]["h"]
            )
            frames[idx] = spritesheet.subsurface(rect).copy()
            durations[idx] = v.get("duration", 100)

        #getting sprite size of first frame, because all frames should be the same size
        sprite_w = data["frames"]["0"]["frame"]["w"]
        sprite_h = data["frames"]["0"]["frame"]["h"]

        #load frameTags
        tags_list = data.get("meta", {}).get("frameTags", [])

        # --- enforce unique tag names and convert them to a dict ---
        seen = set()
        tags = {}

        for tag in tags_list:
            tag_name = tag["name"]   # <--- use a different variable
            if tag_name in seen:
                raise ValueError(f"Duplicate tag name '{tag_name}' in spritesheet '{name}'")
            seen.add(tag_name)
            tags[tag_name] = tag

        self.animations[name] = {
            "frames": frames,
            "durations": durations,
            "tags": tags,
            "sprite_size": (sprite_w, sprite_h)
        }

    # --- SINGLE PNG ---
    def load_png(self, name: str, image_path: str):
        if name in self.animations:
            raise ValueError(f"Spritesheet with name '{name}' already loaded.")

        image = pygame.image.load(image_path).convert_alpha()

        self.animations[name] = {
            "frames": {0: image},
            "durations": {0: 0},
            "tags": {},
            "sprite_size": image.get_size()
        }

    def get_animation_instance(self, name: str) -> "AnimationData":
        base = self.animations[name]
        anim = AnimationData(
            base["frames"],
            base["durations"],
            base["tags"],
            base["sprite_size"]
        )
        anim.base_name = name
        return anim

    def get_rotated_frame(self, anim_name: str, frame_idx: int,
                          angle: int, flip_x: bool = False, flip_y: bool = False):

        key = (anim_name, frame_idx, angle, flip_x, flip_y)

        if key in self._rotation_cache:
            return self._rotation_cache[key]

        base = self.animations[anim_name]
        frame = base["frames"][frame_idx]

        # Rotate around center
        rotated = pygame.transform.rotate(frame, angle)
        rect = rotated.get_rect(center=frame.get_rect().center)

        # Create a new surface to hold the rotated image
        final_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        final_surf.blit(rotated, rect.topleft)

        # Apply flipping if needed
        if flip_x or flip_y:
            final_surf = pygame.transform.flip(final_surf, flip_x, flip_y)

        self._rotation_cache[key] = final_surf
        return final_surf
