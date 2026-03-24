from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from sprite import Sprite
from physics_components import FighterPhysicsComponent



class PlayingState(GameState):

    def enter(self):
        #create a game object and add sprite
        myGameObject = GameObject((0, 0)).add_sprite(Sprite().set_anim_name("nesFighter").set_frame_tag("Idle"))

        myGameObject2 = GameObject((100, 0)).add_sprite(Sprite().set_anim_name("gbFighter").set_frame_tag("Idle"))
        myGameObject2.sprites[0].flip_x = True

        # add physics
        physics = FighterPhysicsComponent()
        myGameObject.set_physics(physics)

        physics2 = FighterPhysicsComponent()
        myGameObject2.set_physics(physics2) 

        self.player1 = myGameObject
        self.player2 = myGameObject2


        for i in range(5):
            self.add_game_object(GameObject((i * 30, 0)).add_sprite(Sprite().set_anim_name("gbFighter").set_frame_tag("Idle")))

        self.sound_manager.play_music("darkchurch")

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_pressed_actions(0)


        # Horizontal movement
        if Action.LEFT in actions:
            self.player1.physics.move_left()
        elif Action.RIGHT in actions:
            self.player1.physics.move_right()
        else:
            # Neither LEFT nor RIGHT is being pressed
            self.player1.physics.stop()

        
        # Vertical movement
        if Action.UP in actions:
            self.player1.physics.move_up()

        

    def update(self, dt):
        super().update(dt)

    def draw(self):
        super().draw()

    def debug_draw(self):
        self.player1.draw_debug(self.view_manager.debug_surface)

