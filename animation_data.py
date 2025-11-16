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
