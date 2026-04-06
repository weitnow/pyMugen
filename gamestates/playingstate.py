from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from gameobjects.sprite import Sprite
from physics_components import FighterPhysicsComponent



class PlayingState(GameState):

    def enter(self):
        #create a game object and add sprite
        myGameObject = GameObject((32, 155-32), origin_center_bottom=True).add_sprite(Sprite().set_anim_name("nesFighter").set_frame_tag("Idle"))
        myGameObject2 = (GameObject((200, 155-32), origin_center_bottom=True)
                        .add_sprite(Sprite()
                        .set_anim_name("nesFighter")
                        .set_frame_tag("Idle")))
        myGameObject2.sprites[0].flip_x = True # just for testing, can be set in the spritesheet data later for convenience
       

        self.player1 = myGameObject
        self.player2 = myGameObject2


        self.sound_manager.play_music("darkchurch")

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_pressed_actions(0)


        

    def update(self, dt):
        self.view_manager.camera.update(self.player1, self.player2) # simple camera follow for testing, can be expanded later for more complex behavior (like lookahead, shake, etc)
        super().update(dt)

        



    def draw(self):
        super().draw()



    def debug_draw(self):
        super().debug_draw()

    

