from gameobject import GameObject
from inputmanager import PlayerController, Action

class Fighter(GameObject):
    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, rotatable=True)
        self.origin_center_bottom = True
        self.controller = PlayerController()

    def update(self, dt):

        actions = self.controller.actions # has a dict like {Action.RIGHT: True, Action.LEFT: False, Action.B: True, ...}

        # Horizontal movement
        if actions[Action.RIGHT]:
            self.pos.x += self.speed * dt
        if actions[Action.LEFT]:
            self.pos.x -= self.speed * dt

        # Jump
        if actions[Action.UP] and self.on_ground:
            self.vel.y = self.jump_velocity
            self.on_ground = False

        super().update(dt) # update physics and animation
        
