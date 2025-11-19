from gameobjects.game_object import GameObject
from input_manager import PlayerController, Action

class Fighter(GameObject):
    def __init__(self, pos: tuple[float, float], player_index: int = 0):
        super().__init__(pos)
        self.origin_center_bottom = True
        self.rotatable = True

        # Movement attributes
        self.speed = 0.1
        self.jump_velocity = -0.4
        self.on_ground = True
        self.facing_right = True

        # Special move list
        self.special_movelist: dict[str, list[Action]] = {
            "Fireball": [Action.DOWN, Action.DOWN_RIGHT, Action.RIGHT, Action.A],
            "Shoryuken": [Action.RIGHT, Action.DOWN, Action.DOWN_RIGHT, Action.A],
            "Sonic Boom": [Action.LEFT, Action.RIGHT, Action.A],
            "Super Kick": [Action.DOWN, Action.UP, Action.A],
        }

        # Controller
        self.controller = PlayerController(player_index, self)

    def update(self, dt):
        actions = self.controller.actions

        # Horizontal movement
        if actions.get(Action.RIGHT, False):
            self.pos.x += self.speed * dt
            self.facing_right = True
        if actions.get(Action.LEFT, False):
            self.pos.x -= self.speed * dt
            self.facing_right = False

        # Jump
        if actions.get(Action.UP, False) and self.on_ground:
            self.vel.y = self.jump_velocity
            self.on_ground = False

        # Call GameObject update (physics + sprite animation)
        super().update(dt)
        
