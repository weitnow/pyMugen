from gameobjects.sprite import RenderAnchor
from gameobjects.game_object import GameObject
from managers.input_manager import Action
from gameobjects.components.player_controller_component import PlayerController
from gameobjects.components.physics_components import FighterPhysicsComponent

class Fighter(GameObject):
    def __init__(self, world_pos, player_index: int = 0):
        super().__init__(world_pos, render_anchor=RenderAnchor.BOTTOMCENTER)
    
        self.enable_camera()

        # Movement attributes
        self.speed = 100
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

        self.add_physics(FighterPhysicsComponent())

        # Add a PlayerController
        self.player_controller = PlayerController(player_index, self)

    def update(self, dt):
        # Update player controller
        if self.player_controller:
            self.player_controller.update(dt)

        # Get current actions from player controller
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
        
