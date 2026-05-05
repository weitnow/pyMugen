from gameobjects.sprite import RenderAnchor
from gameobjects.game_object import GameObject
from managers.input_manager import Action
from components.player_controller_component import PlayerController

class Fighter(GameObject):
    def __init__(self, world_pos, player_index: int = 0):
        super().__init__(world_pos, render_anchor=RenderAnchor.BOTTOMCENTER)
    

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
        self.player_controller = PlayerController(player_index, self)

    def update(self, dt):
        # Player controller updates if there is a player controller attached
        if self.player_controller:
            self.player_controller.update(dt)
            
        actions = self.player_controller.actions

        # Horizontal movement
        if actions.get(Action.RIGHT, False):
            print("Right pressed")
            self.world_pos.x += self.speed * dt
            self.facing_right = True
        if actions.get(Action.LEFT, False):
            print("Left pressed")
            self.world_pos.x -= self.speed * dt
            self.facing_right = False

        

        # Jump
        if actions.get(Action.UP, False) and self.on_ground:
            self.vel.y = self.jump_velocity
            self.on_ground = False

        # Call GameObject update (physics + sprite animation)
        super().update(dt)
        
