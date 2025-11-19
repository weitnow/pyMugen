class PhysicsComponent:
    def __init__(self, gravity=0.001, ground_y=140):
        self.owner = None
        self.gravity = gravity
        self.ground_y = ground_y

    def update(self, dt):
        self.owner.vel.y += self.gravity * dt
        self.owner.pos += self.owner.vel * dt

        if self.owner.pos.y >= self.ground_y:
            self.owner.pos.y = self.ground_y
            self.owner.vel.y = 0
