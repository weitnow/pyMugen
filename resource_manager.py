import json
import pygame
import copy
from typing import Dict
from decorators import singleton


class AnimationData:
    def __init__(self, frames: Dict[int, pygame.Surface], durations: Dict[int, int], tags: Dict[str, dict], sprite_size: tuple, base_name: str, png: bool):

        self.base_name = base_name                         # name of the spritesheet this animation belongs to
        self.frames = frames                # int -> Surface
        self.durations = durations              # int -> duration in ms
        self.tags = tags                       # str -> {"from": int, "to": int}
        self.sprite_size = sprite_size                   # (width, height)
        self.png = png                                    # True if this is a single PNG, False if it is an animation
        
        # Offset storage
        self._global_offset = (0, 0)   
        self._tag_offsets = {}         # tag → (x, y)
        self._frame_offsets = {}       # frame_idx → (x, y)
        self.final_offsets = {}       # frame_idx → (x, y)      this is passed as reference to sprite objects

    # ------------------------------------------------------------------
    # OFFSET SETTERS (clean and simple)
    # ------------------------------------------------------------------
    def set_global_offset(self, x=0, y=0):
        self._global_offset = (x, y)
        self._rebuild_offsets()

    def set_tag_offset(self, tag_name: str, x=0, y=0):
        if tag_name not in self.tags:
            raise ValueError(f"Tag '{tag_name}' does not exist in animation.")
        self._tag_offsets[tag_name] = (x, y)
        self._rebuild_offsets()

    def set_frame_offset(self, frame_idx: int, x=0, y=0):
        if frame_idx not in self.frames:
            raise ValueError(f"Frame {frame_idx} does not exist.")
        self._frame_offsets[frame_idx] = (x, y)
        self._rebuild_offsets()

    # ------------------------------------------------------------------
    # INTERNAL: Build final offset lookup table
    # ------------------------------------------------------------------
    def _rebuild_offsets(self):
        
        self.final_offsets = {}
        frame_to_tag: dict[int, str] = {}

        # Map frames to first tag, warn on overlap
        for tag_name, info in self.tags.items():
            for idx in range(info["from"], info["to"] + 1):
                if idx in frame_to_tag:
                    existing_tag = frame_to_tag[idx]
                    print(
                        f"⚠️ Warning: Frame {idx} in '{self.base_name}' belongs to multiple tags: "
                        f"'{existing_tag}' and '{tag_name}'. Using '{existing_tag}' for offset calculation."
                    )
                    continue  # preserve first tag
                frame_to_tag[idx] = tag_name

        gx, gy = self._global_offset

        # Compute combined offsets
        for idx in self.frames:
            # Global
            fx, fy = gx, gy

            # Tag
            tag_name = frame_to_tag.get(idx)
            if tag_name:
                tx, ty = self._tag_offsets.get(tag_name, (0, 0))
                fx += tx
                fy += ty

            # Frame
            frame_offset = self._frame_offsets.get(idx, (0, 0))
            fx += frame_offset[0]
            fy += frame_offset[1]

            self.final_offsets[idx] = (fx, fy)


@singleton
class ResourceManager:
    def __init__(self):
        self.animations = {}        # name -> AnimationData
        self._rotation_cache = {}   # shared cache across all objects

    def load_spritesheet(self, name: str, image_path: str, json_path: str):
        if name in self.animations:
            raise ValueError(f"Animation '{name}' already loaded.")

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
        
        # Get sprite size from first frame
        sprite_size = (data["frames"]["0"]["frame"]["w"], data["frames"]["0"]["frame"]["h"])

        tags_list = data.get("meta", {}).get("frameTags", [])
        seen = set()
        tags = {}
        for tag in tags_list:
            tag_name = tag["name"]
            if tag_name in seen:
                raise ValueError(f"Duplicate tag name '{tag_name}' in spritesheet '{name}'")
            seen.add(tag_name)
            tags[tag_name] = tag

        # --- Create AnimationData instance ---
        anim = AnimationData(frames, durations, tags, sprite_size, name, png=False)

        # --- Store the AnimationData instance ---
        self.animations[name] = anim

        

    # --- SINGLE PNG ---
    def load_png(self, name: str, image_path: str):
        if name in self.animations:
            raise ValueError(f"Spritesheet with name '{name}' already loaded.")

        image = pygame.image.load(image_path).convert_alpha()

        # fill in data
        frames = {0: image}
        durations = {0: 0}
        tags = {}
        sprite_size= image.get_size()

        # --- Create AnimationData instance ---
        anim = AnimationData(frames, durations, tags, sprite_size, name, png=True)

        # --- Store the AnimationData instance ---
        self.animations[name] = anim

    # ------------------------------------------------------------------
    # CLEAN OFFSET API (delegates to AnimationData)
    # ------------------------------------------------------------------
    def set_global_offset(self, base_name: str, x: int = 0, y: int = 0):
        """Set a global (x,y) offset for the animation."""
        anim = self._require_anim(base_name)
        anim.set_global_offset(x, y)

    def set_tag_offset(self, base_name: str, tag_name: str, x: int = 0, y: int = 0):
        """Set a tag-specific (x,y) offset."""
        anim = self._require_anim(base_name)
        anim.set_tag_offset(tag_name, x, y)

    def set_frame_offset(self, base_name: str, frame_idx: int, x: int = 0, y: int = 0):
        """Set a frame-specific (x,y) offset."""
        anim = self._require_anim(base_name)
        anim.set_frame_offset(frame_idx, x, y)

    def _require_anim(self, name: str):
        """Internal helper to validate animation existence."""
        if name not in self.animations:
            raise ValueError(f"Animation '{name}' not loaded.")
        return self.animations[name]

    
    def get_animationdata_reference(self, name: str) -> "AnimationData":
        """Return a reference to the existing AnimationData instance."""
        if name not in self.animations:
            raise ValueError(f"Animation '{name}' doesn't exisit.")
        return self.animations[name]
    

    def get_rotated_frame(self, anim_name: str, frame_idx: int, angle: int, flip_x: bool = False, flip_y: bool = False):
        base: AnimationData = self.animations[anim_name]
        key = (anim_name, frame_idx, angle, flip_x, flip_y)
        
        if key in self._rotation_cache:
            return self._rotation_cache[key]
        
        frame = base.frames[frame_idx]
        
        # Apply flipping first if requested
        if flip_x or flip_y:
            frame = pygame.transform.flip(frame, flip_x, flip_y)
        
        # Rotate around the sprite center
        fw, fh = frame.get_size()
        pivot = (fw / 2, fh / 2)
        
        # Create a temporary surface large enough to hold the sprite with pivot centered
        tmp_w = int(fw * 3)
        tmp_h = int(fh * 3)
        tmp = pygame.Surface((tmp_w, tmp_h), pygame.SRCALPHA)
        
        # Blit the frame so that pivot maps to the center of tmp
        center_x, center_y = tmp_w // 2, tmp_h // 2
        blit_x = int(center_x - pivot[0])
        blit_y = int(center_y - pivot[1])
        tmp.blit(frame, (blit_x, blit_y))
        
        # Rotate the temporary surface
        rotated = pygame.transform.rotate(tmp, angle)
        
        # Crop to content to remove excessive transparent border
        bbox = rotated.get_bounding_rect()
        
        if bbox.width == 0 or bbox.height == 0:
            final_surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        else:
            final_surf = pygame.Surface((bbox.width, bbox.height), pygame.SRCALPHA)
            final_surf.blit(rotated, (0, 0), bbox)
        
        # Cache and return
        self._rotation_cache[key] = final_surf
        return final_surf



