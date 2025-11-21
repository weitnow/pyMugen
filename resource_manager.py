import json
import pygame
import copy
from typing import Dict
from decorators import singleton

class AnimationData:
    def __init__(self, frames: Dict[int, pygame.Surface], durations: Dict[int, int] = None, tags: Dict[str, dict] = None, sprite_size: tuple = (0,0)):

        # self.frames is a dict mapping frame index to Surface
        self.frames = frames                # int -> Surface
        self.durations = durations              # int -> duration in ms
        self.tags = tags                       # str -> {"from": int, "to": int}
        # --- Offset system --- # offsets are additive                      
        self.global_offset = None                               # (x, y)
        self.tag_offsets = {}                             # tag_name -> (x, y)
        self.frame_offsets = {}                           # frame_idx -> (x, y)    
        # ---------------------        
        self.sprite_size = sprite_size                   # (width, height)

        self.current_tag = None
        self.current_frame_idx = 0
        self.timer = 0
        self.playing = False


    # ---------------------------------------------------------
    # OFFSET SETTER
    # ---------------------------------------------------------
    def set_offset(self, *, global_offset=False, tag=None, frame=None, x=None, y=None):
        """
        Add offset to global / tag / frame.
        additive: final = global + tag + frame.
        Missing coordinates default to 0.
        Overwriting is forbidden -> raises Exception.
        Examples:
            set_offset(global_offset=True, x=5, y=10)
            set_offset(tag="Idle", x=-3)
            set_offset(frame=2, y=4)
        """

        # ---------- Validate mode ----------
        modes_selected = sum([
            1 if global_offset else 0,
            1 if tag is not None else 0,
            1 if frame is not None else 0
        ])
        if modes_selected != 1:
            raise ValueError("set_offset() requires exactly one of: global_offset=True, tag=..., frame=...")

        # Missing coordinates default to zero
        ox = 0 if x is None else x
        oy = 0 if y is None else y
        new_offset = (ox, oy)

        # ---------- Global offset ----------
        if global_offset:
            if self.global_offset is not None:
                raise ValueError("Global offset already exists and cannot be overwritten.")
            self.global_offset = new_offset
            return

        # ---------- Tag offset ----------
        if tag is not None:
            if tag not in self.tags:
                raise ValueError(f"Tag '{tag}' not found in animation.")
            
            if tag in self.tag_offsets:
                raise ValueError(f"Offset for tag '{tag}' already exists and cannot be overwritten.")
            
            self.tag_offsets[tag] = new_offset
            return

        # ---------- Frame offset ----------
        if frame is not None:
            if frame not in self.frames:
                raise ValueError(f"Frame '{frame}' does not exist in animation frames.")
            
            if frame in self.frame_offsets:
                raise ValueError(f"Offset for frame '{frame}' already exists and cannot be overwritten.")

            self.frame_offsets[frame] = new_offset
            return

    # ---------------------------------------------------------
    # OFFSET GETTERS
    # ---------------------------------------------------------
    def get_global_offset(self):
        return self.global_offset if self.global_offset is not None else (0, 0)

    def get_tag_offset(self):
        if self.current_tag is None:
            return (0, 0)
        tag_name = self.current_tag["name"]
        return self.tag_offsets.get(tag_name, (0, 0))

    def get_frame_offset(self):
        return self.frame_offsets.get(self.current_frame_idx, (0, 0))

    # ---------------------------------------------------------
    # FINAL OFFSET
    # ---------------------------------------------------------
    def get_current_offset(self):
        gx, gy = self.get_global_offset()
        tx, ty = self.get_tag_offset()
        fx, fy = self.get_frame_offset()
        return (gx + tx + fx, gy + ty + fy)

    # ---------------------------------------------------------
    # TAG SYSTEM
    # --------------------------------------------------------

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

        # --- Create AnimationData instance ---
        anim = AnimationData(frames, durations, tags, (sprite_w, sprite_h))
        #anim.base_name = name #TODO: needed?

        # --- Store the instance in self.animations ---
        self.animations[name] = anim
        

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

    # --- SET OFFSET of ANIMATION, do this immidiatly after loading a spritesheet or a png---
    def set_offset(self, *, base_name: str, global_offset=False, tag=None, frame=None, x=None, y=None):
        """
        Set an offset on an animation by base_name.
        Mirrors AnimationData.set_offset().
        """
        if base_name not in self.animations:
            raise ValueError(f"Animation '{base_name}' not loaded.")

        # Modify the stored AnimationData instance directly. Previously this
        # used get_animation_instance() which returned a deepcopy, so changes
        # were applied to the copy and lost.
        anim = self.animations[base_name]
        # If stored entry is a dict (legacy), try to normalize it first.
        if not isinstance(anim, AnimationData):
            # convert legacy dict to AnimationData
            frames = anim.get("frames", {})
            durations = anim.get("durations", {})
            tags = anim.get("tags", {})
            sprite_size = anim.get("sprite_size", (0, 0))
            anim = AnimationData(frames, durations, tags, sprite_size)
            self.animations[base_name] = anim

        anim.set_offset(global_offset=global_offset, tag=tag, frame=frame, x=x, y=y)


    def get_animation_instance(self, name: str) -> "AnimationData":
        """Return a copy of the existing AnimationData instance."""
        if name not in self.animations:
            raise ValueError(f"Animation '{name}' not loaded.")
        # Return a deep copy so callers can mutate the returned instance safely
        # without affecting the canonical stored animation.
        return copy.deepcopy(self.animations[name])
    
  

    def get_rotated_frame(self, anim_name: str, frame_idx: int,
                          angle: int, flip_x: bool = False, flip_y: bool = False):

        key = (anim_name, frame_idx, angle, flip_x, flip_y)

        if key in self._rotation_cache:
            return self._rotation_cache[key]

        base = self.animations[anim_name]
        # support both AnimationData instances and legacy dict storage
        if isinstance(base, AnimationData):
            frame = base.frames[frame_idx]
        else:
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
