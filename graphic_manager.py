import json
import pygame
from typing import Dict
from decorators import singleton
import globals


class AnimationData:
    def __init__(self, frames: Dict[int, pygame.Surface], durations: Dict[int, int], tags: Dict[str, dict], sprite_size: tuple, base_name: str, png: bool, scale: int):

        self.base_name = base_name                         # name of the spritesheet this animation belongs to
        self.frames = frames                # int -> Surface
        self.durations = durations              # int -> duration in ms
        self.tags = tags                       # str -> {"from": int, "to": int}
        self.sprite_size = sprite_size                   # (width, height)
        self.png = png                                    # True if this is a single PNG, False if it is an animation
        self.scale = scale                                 # the scale factor 
        
        # Offset storage
        self._global_offset = (0, 0)   
        self._tag_offsets = {}         # tag → (x, y)
        self._frame_offsets = {}       # frame_idx → (x, y)
        self.final_offsets = {}       # frame_idx → (x, y)      this is passed as reference to sprite objects

        # Private attributes
        self._source_image_path = None  # is set by GraphicManager when loading
        self._source_json_path = None   # is set by GraphicManager when loading

    # ------------------------------------------------------------------
    # OFFSET SETTERS (clean and simple)
    # ------------------------------------------------------------------
    def set_global_offset(self, x, y):
        self._global_offset = (x, y)
        self._rebuild_offsets()

    def set_tag_offset(self, tag_name: str, x, y):
        if tag_name not in self.tags:
            raise ValueError(f"Tag '{tag_name}' does not exist in animation.")
        self._tag_offsets[tag_name] = (x, y)
        self._rebuild_offsets()

    def set_frame_offset(self, frame_idx: int, x, y):
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
class GraphicManager:
    def __init__(self):
        self.animations = {}        # name -> AnimationData
        self._rotation_cache = {}   # shared cache across all objects

        self.convert_alpha = True  # whether to convert images with alpha

    def load_spritesheet(self, name: str, image_path: str, json_path: str, scale: int = 1):
        if name in self.animations and scale in self.animations[name]:
            raise ValueError(f"Animation '{name}' with scale {scale} already loaded.")

        with open(json_path, "r") as f:
            data = json.load(f)

        img = pygame.image.load(image_path)
        spritesheet = img.convert_alpha() if self.convert_alpha else img.convert()

        frames = {}
        durations = {}

        for k, v in data["frames"].items():
            idx = int(k)
            rect = pygame.Rect(v["frame"]["x"], v["frame"]["y"], v["frame"]["w"], v["frame"]["h"])
            frame = spritesheet.subsurface(rect).copy()
            if scale != 1:
                new_size = (int(rect.width * scale), int(rect.height * scale))
                frame = pygame.transform.scale(frame, new_size)
            frames[idx] = frame
            durations[idx] = v.get("duration", 100)
        
        # Get sprite size from first frame
        sprite_size = frames[0].get_size() if frames else (0, 0)

        tags_list = data.get("meta", {}).get("frameTags", [])
        seen = set()
        tags = {}
        for tag in tags_list:
            tag_name = tag["name"]
            if tag_name in seen:
                raise ValueError(f"Duplicate tag name '{tag_name}' in spritesheet '{name}'")
            seen.add(tag_name)
            tags[tag_name] = tag

        # ensure outer dict
        if name not in self.animations:
            self.animations[name] = {}

        # create base (scale 1) if missing
        if 1 not in self.animations[name]:
            base_frames = {}
            for k, v in data["frames"].items():
                idx = int(k)
                rect = pygame.Rect(v["frame"]["x"], v["frame"]["y"], v["frame"]["w"], v["frame"]["h"])
                base_frames[idx] = spritesheet.subsurface(rect).copy()

            base_anim = AnimationData(base_frames, durations, tags,
                                    base_frames[0].get_size() if base_frames else (0, 0),
                                    name, png=False, scale=1)
            
            base_anim._source_image_path = image_path  # store source path for reference
            base_anim._source_json_path = json_path    # store source path for reference

            self.animations[name][1] = base_anim

        # create requested scale if missing
        if scale not in self.animations[name]:
            if scale == 1:
                return

            scaled_frames = {}
            for idx, frame in self.animations[name][1].frames.items():
                new_size = (int(frame.get_width() * scale), int(frame.get_height() * scale))
                scaled_frames[idx] = pygame.transform.scale(frame, new_size)

            scaled_anim = AnimationData(
                scaled_frames,
                durations,
                tags,
                scaled_frames[0].get_size() if scaled_frames else (0, 0),
                name,
                png=False,
                scale=scale
            )

            scaled_anim._source_image_path = self.animations[name][1]._source_image_path  # reference original source
            scaled_anim._source_json_path = self.animations[name][1]._source_json_path    # reference original source

            self.animations[name][scale] = scaled_anim

        

    # --- SINGLE PNG ---
    def load_png(self, name: str, image_path: str, scale: int = 1):
        if name in self.animations and scale in self.animations[name]:
            raise ValueError(f"PNG '{name}' with scale {scale} already loaded.")

        img = pygame.image.load(image_path)
        base_image = img.convert_alpha() if self.convert_alpha else img.convert()

        # create outer dictionary
        if name not in self.animations:
            self.animations[name] = {}

        # always create/store scale 1
        if 1 not in self.animations[name]:
            base_anim = AnimationData(
                frames={0: base_image},
                durations={0: 0},
                tags={},
                sprite_size=base_image.get_size(),
                base_name=name,
                png=True,
                scale=1
            )

            base_anim._source_image_path = image_path  # store source path for reference

            self.animations[name][1] = base_anim

        # create requested scale if needed
        if scale != 1 and scale not in self.animations[name]:
            new_size = (
                int(base_image.get_width() * scale),
                int(base_image.get_height() * scale)
            )

            scaled_image = pygame.transform.scale(base_image, new_size)

            scaled_anim = AnimationData(
                frames={0: scaled_image},
                durations={0: 0},
                tags={},
                sprite_size=scaled_image.get_size(),
                base_name=name,
                png=True,
                scale=scale
            )

            scaled_anim._source_image_path = self.animations[name][1]._source_image_path  # reference original source

            self.animations[name][scale] = scaled_anim

    # ------------------------------------------------------------------
    # CLEAN OFFSET API (delegates to AnimationData)
    # ------------------------------------------------------------------
    def set_global_offset(self, base_name: str, x: int, y: int, scale: int):
        """Set a global (x,y) offset for the animation."""
        anim = self._require_anim(base_name, scale)
        anim.set_global_offset(x, y, scale)

    def set_tag_offset(self, base_name: str, tag_name: str, x: int, y: int, scale: int):
        """Set a tag-specific (x,y) offset."""
        anim = self._require_anim(base_name, scale)
        anim.set_tag_offset(tag_name, x, y, scale)

    def set_frame_offset(self, base_name: str, frame_idx: int, x: int, y: int, scale: int):
        """Set a frame-specific (x,y) offset."""
        anim = self._require_anim(base_name, scale)
        anim.set_frame_offset(frame_idx, x, y, scale)

    def _require_anim(self, name: str, scale: int) -> "AnimationData":
        """Internal helper to validate animation existence."""
        if scale not in self.animations[name]:
            raise ValueError(f"Animation '{name}' with scale {scale} not loaded.")
        return self.animations[name][scale]

    
    def get_animationdata_reference(self, name: str, scale: int) -> "AnimationData":
        """Return a reference to the existing AnimationData instance."""
        if scale not in self.animations[name]:
            raise ValueError(f"Animation '{name}' with scale {scale} not loaded.")
        return self.animations[name][scale]
    
        
    def get_rotated_frame(
        self,
        anim_name: str,
        frame_idx: int,
        angle: int,
        flip_x: bool,
        flip_y: bool,
        scale: int
    ):

        original = self.animations[anim_name][scale].frames[frame_idx]

        key = (anim_name, frame_idx, angle, flip_x, flip_y, scale)

        if key in self._rotation_cache:
            return self._rotation_cache[key]

        # 1. flip first
        working = pygame.transform.flip(original, flip_x, flip_y) if (flip_x or flip_y) else original

        # 2. no rotation
        if angle == 0:
            self._rotation_cache[key] = working
            return working

        # 3. rotate
        rotated = pygame.transform.rotate(working, angle)

        # 4. IMPORTANT:
        # No offset correction anymore.
        # We rely on center-based rect placement in Sprite.draw()
        self._rotation_cache[key] = rotated

        return rotated
    
    def get_or_create_scaled(self, name: str, scale: int):
        """
        Ensure scale `factor` exists for animation `name`.
        Derives from the scale=1 version, copying offsets proportionally.
        """
        if name not in self.animations:
            raise ValueError(f"Animation '{name}' not loaded.")
        if scale in self.animations[name]:
            return  # already exists

        source = self.animations[name][1]  # always derive from scale=1

        if source.png:
            self.load_png(name, source._source_image_path, scale=scale)
        else:
            self.load_spritesheet(name, source._source_image_path, source._source_json_path, scale=scale)

        scaled = self.animations[name][scale]

        # Copy offsets proportionally from scale=1
        gx, gy = source._global_offset
        if gx != 0 or gy != 0:
            scaled.set_global_offset(int(gx * scale), int(gy * scale))

        for tag_name, (tx, ty) in source._tag_offsets.items():
            if tx != 0 or ty != 0:
                scaled.set_tag_offset(tag_name, int(tx * scale), int(ty * scale))

        for frame_idx, (fx, fy) in source._frame_offsets.items():
            if fx != 0 or fy != 0:
                scaled.set_frame_offset(frame_idx, int(fx * scale), int(fy * scale))
    






