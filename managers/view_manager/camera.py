import pygame
import random

class Camera:
    def __init__(self, view_width, view_height):
        self.view_width = view_width
        self.view_height = view_height
        self.world_width = 0    # will be set by the stage, but we initialize it to 0 here #1200
        self.world_height = 0   # will be set by the stage, but we initialize it to 0 here #420
        self.world_center_x = 0 # will be set by the stage, but we initialize it to 0 here #600
        self.world_center_y = 0 # will be set by the stage, but we initialize it to 0 here #210

        # Cam should be clampet to -213 and +213 on x because the stage is 1200 wide and the view is 774 wide, so 1200-774=426, and half of that is 213. We can see 94 pixels of the left wall and 94 pixels of the right wall, so we can move the camera 94 pixels in either direction before we start seeing empty space. So the camera's center can move 212 pixels to the left and 212 pixels to the right from the center of the stage.

        self._x = 0.0
        self._y = 0.0

        self.follow_enabled = True
        self.clamp_to_world = False # only relevant for manual movement of camera with property x and y, not the built-in follow behavior

        self.smooth_speed = 0.12  # tweak to taste (0.0–1.0 feel)

        # Screenshake (trauma-based)
        self._trauma = 0.0
        self._trauma_decay = 2.5   # trauma/second lost
        self._max_shake_x = 8
        self._max_shake_y = 6
        self._shake_x = 0.0
        self._shake_y = 0.0

    # --------------------------
    # Properties
    # --------------------------
    @property
    def x(self): return self._x
    @x.setter
    def x(self, value):
        self._x = value
        if self.clamp_to_world:
            self._x = max(0.0, min(self._x, self.world_width - self.view_width))

    @property
    def y(self): return self._y
    @y.setter
    def y(self, value):
        self._y = value
        if self.clamp_to_world:
            self._y = max(0.0, min(self._y, self.world_height - self.view_height))


    # --------------------------
    # Public API
    # --------------------------
    def add_trauma(self, amount: float):
        """Add screenshake trauma. 0.0–1.0, stacks up to 1."""
        self._trauma = min(1.0, self._trauma + amount)

    def update(self, dt: float, p1, p2):
        if self.follow_enabled:
            self._update_follow(dt, p1, p2)
        self._update_shake(dt)

    def apply_vec2(self, pos, shake_factor: float = 1.0) -> pygame.Vector2:
        shake_x = self._shake_x * shake_factor
        shake_y = self._shake_y * shake_factor
        return pygame.Vector2(pos) - pygame.Vector2(self._x - shake_x, self._y - shake_y)
    


    # --------------------------
    # Private
    # --------------------------
    def _update_follow(self, dt: float, p1, p2):
        mid_x = (p1.world_pos.x + p2.world_pos.x) / 2
        mid_y = (p1.world_pos.y + p2.world_pos.y) / 2

        target_x = mid_x - self.view_width / 2
        target_y = mid_y - self.view_height / 2

        # Soft vertical bias when either player is airborne
        airborne_bias = -18 if (not p1.on_ground or not p2.on_ground) else 0
        target_y += airborne_bias

        # Clamp to world bounds
        target_x = max(0.0, min(target_x, self.world_width - self.view_width))
        target_y = max(0.0, min(target_y, self.world_height - self.view_height))

        # Frame-rate independent lerp
        t = 1.0 - (1.0 - self.smooth_speed) ** (dt * 60)
        self._x += (target_x - self._x) * t
        self.y += (target_y - self.y) * t


    def _update_shake(self, dt: float):
        if self._trauma <= 0.0:
            self._shake_x = 0.0
            self._shake_y = 0.0
            return

        self._trauma = max(0.0, self._trauma - self._trauma_decay * dt)
        shake = self._trauma ** 2  # quadratic feels more natural than linear

        self._shake_x = self._max_shake_x * shake * random.uniform(-1, 1)
        self._shake_y = self._max_shake_y * shake * random.uniform(-1, 1)