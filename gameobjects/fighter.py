from game_object import GameObject
from input_manager import PlayerController, Action

class Fighter(GameObject):
    def __init__(self, pos: tuple[float, float], player_index: int = 0):
        super().__init__(pos, rotatable=True)
        self.origin_center_bottom = True

        # attributes
        self.facing_right: bool = True

        # Specialmovelist
        self.special_movelist: dict[str, list[Action]] = {
            "Fireball": [Action.DOWN, Action.DOWN_RIGHT, Action.RIGHT, Action.A],
            "Shoryuken": [Action.RIGHT, Action.DOWN, Action.DOWN_RIGHT, Action.A],
            "Sonic Boom": [Action.LEFT, Action.RIGHT, Action.A],
            "Super Kick": [Action.DOWN, Action.UP, Action.A],
        }


        self.controller = PlayerController(player_index, self)

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
        
