from gamestates.gamestate_base import GameState
from game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from sprite import Sprite
from physics_component import PhysicsComponent



class PlayingState(GameState):

    def enter(self):
        #create a game object and add sprite
        myGameObject = GameObject((0, 0))
        myGameObject.add_sprite(Sprite().set_anim_name("nesFighter").set_frame_tag("Idle"))


        # add physics
        physics = PhysicsComponent(gravity=980, ground_y= 120, jump_force=-400)
        myGameObject.set_physics(physics)


        self.myGameObject = myGameObject

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        if Action.UP in actions:
            self.myGameObject.physics.jump()

    def update(self, dt):
        self.myGameObject.update(dt)

    def draw(self):
        self.myGameObject.draw(self.view_manager.game_surface)

    def debug_draw(self):
        self.myGameObject.draw_debug(self.view_manager.debug_surface)