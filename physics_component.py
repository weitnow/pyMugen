import pygame

class PhysicsComponent:
    def __init__(self, gravity=980, ground_y=400, jump_force=-400):
        """
        Initialize physics component.
        
        Args:
            gravity: Pixels per second squared (default: 980)
            ground_y: Y position of the ground (default: 400)
            jump_force: Upward velocity applied on jump (negative = up, default: -400)
        """
        self.owner = None
        self.gravity = gravity
        self.ground_y = ground_y
        self.jump_force = jump_force
        self.on_ground = False
        
    def update(self, dt):
        if not self.owner:
            return
        
        # Apply gravity
        self.owner.vel.y += self.gravity * dt
        
        # Update position
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
            self.owner.vel.y = self.jump_force
            self.on_ground = False