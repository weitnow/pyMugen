from typing import Dict, Any, List, Optional
import pygame

class AnimationData:
    def __init__(
        self,
        spritesheet: pygame.Surface,
        frames: Dict[int, pygame.Surface],
        tags: List[dict],
        durations: Optional[Dict[int, int]] = None,
    ):
        self.spritesheet = spritesheet
        # frames: mapping from frame index (int) -> pygame.Surface
        self.frames = frames
        # durations: mapping from frame index (int) -> duration in ms
        self.durations = durations or {}
        self.tags = tags        # [ { "name": "Idle", "from": 0, "to": 2, ... }, ... ]  -> List[dict]
        # Keep frame keys sorted so numeric frame indices map predictably
        self.frame_keys = sorted(list(self.frames.keys()))  # ordered list of frame indices (ints)
        
