class PhysicsComponent:
    def __init__(self, gravity=1180, ground_y=120, jump_speed=400):
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
        self.owner.pos.x += self.owner.vel.x * dt
        
        # Ground collision
        if self.owner.pos.y >= self.ground_y:
            self.owner.pos.y = self.ground_y
            self.owner.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # set horizontal velocity to 0 if no left/right input (friction)
        #self.owner.vel.x *= 0.8  # simple friction effect
            
    def move_up(self):
        """Apply jump force if on ground."""
        if self.on_ground:
            self.owner.vel.y = -self.jump_speed
            self.on_ground = False

class FighterPhysicsComponent(PhysicsComponent):
    def __init__(self, gravity=1180, ground_y=120, jump_speed=400):
        super().__init__(gravity, ground_y, jump_speed)
        # Additional fighter-specific physics properties can be added here

    def move_left(self):
        # Implement left movement logic (e.g., set horizontal velocity)
        self.owner.vel.x = -10  # Example horizontal speed to the left

    def move_right(self):
        # Implement right movement logic (e.g., set horizontal velocity)
        self.owner.vel.x = 10  # Example horizontal speed to the right

    def move_down(self):
        # Implement down movement logic if needed
        pass

    def stop(self):
        # Stop horizontal movement (e.g., when no left/right input)
        self.owner.vel.x = 0

    

    