class PhysicsComponent:
    def __init__(self, gravity=50, ground_y=120, jump_speed=100):
        """
        Initialize physics component with millisecond-based values.
        Args:
            gravity: Pixels per millisecond squared (default: 0.0005)
            ground_y: Y position of the ground (default: 120)
            jump_speed: Initial upward speed in pixels/ms (default: 0.1)
        """
        self.owner = None
        self.gravity = gravity
        self.ground_y = ground_y
        self.jump_speed = jump_speed
        self.on_ground = False
        
    def update(self, dt):
        # Apply gravity and update position
        self.owner.vel.y += self.gravity * dt
        self.owner.pos.y += self.owner.vel.y * dt
        
        # Ground collision
        if self.owner.pos.y >= self.ground_y:
            self.owner.pos.y = self.ground_y
            self.owner.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
    def jump(self):
        """Apply jump force if on ground."""
        if self.on_ground:
            self.owner.vel.y = -self.jump_speed
            self.on_ground = False