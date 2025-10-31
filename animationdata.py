from typing import Dict, Any, List
import pygame

class AnimationData:
    def __init__(self, spritesheet: pygame.Surface, frames: Dict[str, pygame.Surface], tags: List[dict]):
        self.spritesheet = spritesheet
        self.frames = frames    # { "gbFighter 0.aseprite": pygame.Surface, ... }       -> Dict[str, pygame.Surface]
        self.tags = tags        # [ { "name": "Idle", "from": 0, "to": 2, ... }, ... ]  -> List[dict]
        self.frame_keys = list(frames.keys())  # in sorted order    -> List[string], z.B. "gbFighter 0.asperite"
        
