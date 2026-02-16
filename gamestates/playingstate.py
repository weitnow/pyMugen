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



from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject
from input_manager import PlayerController, Action
from sprite import Sprite
from physics_components import FighterPhysicsComponent


class PlayingState_Stresstest(GameState):

    def enter(self):
        self.game_objects = []

        # create 120 objects in a grid
        cols = 12
        spacing_x = 10
        spacing_y = 80

        for i in range(10):
            row = i // cols
            col = i % cols

            x = col * spacing_x
            y = row * spacing_y

            obj = GameObject((x, y))
            obj.add_sprite(
                Sprite()
                .set_anim_name("nesFighter")
                .set_frame_tag("Idle")
            )

            physics = FighterPhysicsComponent()
            obj.set_physics(physics)

            self.game_objects.append(obj)

        # control only the first object
        self.player_object = self.game_objects[0]

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)

        if Action.UP in actions:
            self.player_object.physics.move_up()
            for obj in self.game_objects:
                if obj != self.player_object:
                    obj.physics.move_up()

        if Action.LEFT in actions:
            self.player_object.physics.move_left()

        if Action.RIGHT in actions:
            self.player_object.physics.move_right()

    def update(self, dt):
        for obj in self.game_objects:
            obj.update(dt)

    def draw(self):
        for obj in self.game_objects:
            obj.draw(self.view_manager.game_surface)

    def debug_draw(self):
        for obj in self.game_objects:
            obj.draw_debug(self.view_manager.debug_surface)
