from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from sprite import Sprite
from physics_components import FighterPhysicsComponent



class PlayingState(GameState):

    def enter(self):
        #create a game object and add sprite
        myGameObject = GameObject((0, 0))
        myGameObject.add_sprite(Sprite().set_anim_name("nesFighter").set_frame_tag("Idle"))

        self.sound_manager.play_music("bg_music")


        # add physics
        physics = FighterPhysicsComponent()
        myGameObject.set_physics(physics)


        self.myGameObject = myGameObject

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_pressed_actions(0)


        # Horizontal movement
        if Action.LEFT in actions:
            self.myGameObject.physics.move_left()
        elif Action.RIGHT in actions:
            self.myGameObject.physics.move_right()
        else:
            # Neither LEFT nor RIGHT is being pressed
            self.myGameObject.physics.stop()

        
        # Vertical movement
        if Action.UP in actions:
            self.myGameObject.physics.move_up()

        

    def update(self, dt):
        self.myGameObject.update(dt)

    def draw(self):
        self.myGameObject.draw(self.view_manager.game_surface)

    def debug_draw(self):
        self.myGameObject.draw_debug(self.view_manager.debug_surface)

