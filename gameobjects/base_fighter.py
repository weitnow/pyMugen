from gameobjects.sprite import RenderAnchor
from gameobjects.game_object import GameObject
from managers.input_manager import Action
from gameobjects.components.player_controller_component import PlayerController
from gameobjects.components.physics_components import FighterPhysicsComponent

class BaseFighter(GameObject):
    def __init__(self, world_pos, player_index: int = 0):
        super().__init__(world_pos, render_anchor=RenderAnchor.BOTTOMCENTER)
    
        self.enable_camera()

        # Movement attributes
        self.speed = 100
        self.jump_velocity = -0.4 
        self.facing_right = True

        # Special move list
        self.special_movelist: dict[str, list[Action]] = {
            "Fireball": [Action.DOWN, Action.DOWN_RIGHT, Action.RIGHT, Action.A],
            "Shoryuken": [Action.RIGHT, Action.DOWN, Action.DOWN_RIGHT, Action.A],
            "Sonic Boom": [Action.LEFT, Action.RIGHT, Action.A],
            "Super Kick": [Action.DOWN, Action.UP, Action.A],
        }

        self.add_physics(FighterPhysicsComponent())

        # Add a PlayerController
        self.player_controller = PlayerController(player_index, self)

    def update(self, dt):
        if self.player_controller:
            self.player_controller.update(dt)

        actions = self.player_controller.actions

        # Delegate movement to physics component
        if actions.get(Action.RIGHT, False):
            self.physics.move_right()
            self.facing_right = True
        elif actions.get(Action.LEFT, False):
            self.physics.move_left()
            self.facing_right = False
        else:
            self.physics.stop()

        if actions.get(Action.UP, False):
            self.physics.move_up()  # move_up already checks on_ground internally

        super().update(dt)  # runs physics + sprite animation
        
