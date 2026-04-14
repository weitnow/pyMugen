

from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from gameobjects.sprite import Sprite
from physics_components import FighterPhysicsComponent

from gameobjects.sprite import RenderAnchor



class TestState(GameState):

    def enter(self):
        #create a game object and add sprite
        self.mySprite1 = Sprite().set_anim_name("debug32")
        self.mySprite1.set_frame(1)
        self.mySprite2 = Sprite().set_anim_name("debug32x32")

        self.randoranchor = RenderAnchor.CENTER



       

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)

        if Action.RIGHT in actions:
            self.mySprite1.rotation -= 45
            self.mySprite2.rotation -= 45
            print(self.mySprite1.sprite_size)
        elif Action.LEFT in actions:
            self.mySprite1.rotation += 45
            self.mySprite2.rotation += 45

        if Action.UP in actions:
            # Cycle through render anchors for testing
            if self.randoranchor == RenderAnchor.CENTER:
                self.randoranchor = RenderAnchor.TOPLEFT
            elif self.randoranchor == RenderAnchor.TOPLEFT:
                self.randoranchor = RenderAnchor.BOTTOMMID
            else:
                self.randoranchor = RenderAnchor.CENTER
        


    def update(self, dt):
        #self.view_manager.camera.update(self.player1, self.player2) # simple camera follow for testing, can be expanded later for more complex behavior (like lookahead, shake, etc)
        


        super().update(dt)

    



    def draw(self):
        self.mySprite1.draw(self.view_manager.game_surface, (16, 16), render_anchor=self.randoranchor)
        self.mySprite2.draw(self.view_manager.game_surface, (16+32, 16), render_anchor=self.randoranchor)




        super().draw()



    def debug_draw(self):
        self.mySprite1.debug_draw(self.view_manager.debug_surface, (16, 16), render_anchor=self.randoranchor)
        super().debug_draw()

    

