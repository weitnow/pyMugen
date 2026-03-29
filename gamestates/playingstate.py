from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from gameobjects.sprite import Sprite
from physics_components import FighterPhysicsComponent



class PlayingState(GameState):

    def enter(self):
        #create a game object and add sprite
        myGameObject = GameObject((32, 32)).add_sprite(Sprite().set_anim_name("nesFighter").set_frame_tag("Idle"))

       

        self.player1 = myGameObject

        self.sprite = Sprite().set_anim_name("debug32x32")
   



        self.sound_manager.play_music("darkchurch")

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_pressed_actions(0)


        

    def update(self, dt):
        super().update(dt)

        self.sprite.rotation += 90 * dt # rotate 90 degrees per second



    def draw(self):
        super().draw()

        self.sprite.draw(self.view_manager.game_surface, (100, 100))


    def debug_draw(self):
        self.player1.draw_debug(self.view_manager.debug_surface)

        self.sprite.debug_draw(self.view_manager.debug_surface, (100, 100))

