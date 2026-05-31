import pygame
import random

class Camera:
    def __init__(self, view_width, view_height):
        self.view_width = view_width # 774 is the width of the visible area of the stage, which is 960 game window width minus 94 pixels of left wall and 94 pixels of right wall
        self.view_height = view_height # 368 is the height of the visible area of the stage, which is 540 game window height minus 86 pixels of top wall and 86 pixels of bottom wall
        self.world_width = 0    # will be set by the stage, but we initialize it to 0 here #1200
        self.world_height = 0   # will be set by the stage, but we initialize it to 0 here #420
        self.world_center_x = 0 # will be set by the stage, but we initialize it to 0 here #600
        self.world_center_y = 0 # will be set by the stage, but we initialize it to 0 here #210
        self.x_travel = 0      # how far the camera can move in x from the center of the stage, will be set by the stage based on world width and view width #213
        self.y_travel_min = 0      # how far the camera can move in y from the center of the stage, will be set by the stage based on world height and view height #
        self.y_travel_max = 0      # how far the camera can move in y from the center of the stage, will be set by the stage based on world height and view height #
        # Cam should be clampet to -213 and +213 on x because the stage is 1200 wide and the view is 774 wide, so 1200-774=426, and half of that is 213. We can see 94 pixels of the left wall and 94 pixels of the right wall, so we can move the camera 94 pixels in either direction before we start seeing empty space. So the camera's center can move 212 pixels to the left and 212 pixels to the right from the center of the stage.

        self._x = 0.0
        self._y = 0.0

        self.follow_enabled = True
        self.clamp_to_world = True 

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
            min_x = -self.x_travel 
            max_x = self.x_travel 
            self._x = max(min_x, min(self._x, max_x))

    @property
    def y(self): return self._y
    @y.setter
    def y(self, value):
        self._y = value
        if self.clamp_to_world:
            min_y = self.y_travel_min 
            max_y = self.y_travel_max
            self._y = max(min_y, min(self._y, max_y))   


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

        # Frame-rate independent lerp
        t = 1.0 - (1.0 - self.smooth_speed) ** (dt * 60)
        self.x += (target_x - self._x) * t
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