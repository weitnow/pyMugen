

from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from gameobjects.sprite import Sprite
from physics_components import FighterPhysicsComponent

from gameobjects.sprite import RenderAnchor



class PerformanceTestState(GameState):

    def enter(self):
        #create a game object and add sprite
        self.sprites = []
        self.mySprite1 = Sprite().set_anim_name("debug32")
        self.mySprite1.set_frame(1)

        for i in range(50):
            sprite = Sprite().set_anim_name("nesFighter").set_frame_tag("Idle")
            self.sprites.append(sprite)

        self.randoranchor = RenderAnchor.CENTER



       

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)

        if Action.RIGHT in actions:
            self.mySprite1.rotation -= 45

            for sprite in self.sprites:
                sprite.rotation -= 45

        elif Action.LEFT in actions:
            self.mySprite1.rotation += 45

            for sprite in self.sprites:
                sprite.rotation += 45
 
        if Action.UP in actions:
            # Cycle through render anchors for testing
            if self.randoranchor == RenderAnchor.CENTER:
                self.randoranchor = RenderAnchor.TOPLEFT
            elif self.randoranchor == RenderAnchor.TOPLEFT:
                self.randoranchor = RenderAnchor.BOTTOMCENTER
            else:
                self.randoranchor = RenderAnchor.CENTER

        if Action.DOWN in actions:
            self.mySprite1.flip_x = not self.mySprite1.flip_x

            for sprite in self.sprites:
                sprite.flip_x = not sprite.flip_x
  
        


    def update(self, dt):
        #self.view_manager.camera.update(self.player1, self.player2) # simple camera follow for testing, can be expanded later for more complex behavior (like lookahead, shake, etc)
        
        for sprite in self.sprites:
            sprite.update(dt)

        super().update(dt)

    



    def draw(self):
        self.mySprite1.draw(self.view_manager.game_surface, (16, 16), render_anchor=self.randoranchor)


        for i, sprite in enumerate(self.sprites):
            x = 16 + (i % 20) * 32
            y = 64 + (i // 20) * 32
            sprite.draw(self.view_manager.game_surface, (x, y), render_anchor=self.randoranchor)

        super().draw()



    def debug_draw(self):
        self.mySprite1.debug_draw(self.view_manager.debug_surface, (16, 16), render_anchor=self.randoranchor)

        for i, sprite in enumerate(self.sprites):
            x = 16 + (i % 20) * 32
            y = 64 + (i // 20) * 32
            sprite.debug_draw(self.view_manager.debug_surface, (x, y), render_anchor=self.randoranchor)
        super().debug_draw()

    

