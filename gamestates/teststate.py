

from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import Action
from gameobjects.sprite import Sprite
from gameobjects.components.physics_components import FighterPhysicsComponent
from gameobjects.components.player_controller_component import PlayerController
import pygame

from gameobjects.sprite import RenderAnchor



class TestState(GameState):

    def enter(self):
        #create a game object and add sprite

        self.anchor = RenderAnchor.CENTER
        self.mySprite1 = Sprite().set_anim_name("debug32")
        self.mySprite1.set_frame(0)

        


 

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        actions_held = self.input_manager.get_pressed_actions(0)

        if Action.RIGHT in actions_held:
            #rotate sprite
            self.mySprite1.rotation += 2

        elif Action.LEFT in actions_held:
            self.mySprite1.rotation -= 2
        else:
            pass
 
        if Action.UP in actions:
            pass

        if Action.DOWN in actions:
            # cycle through anchors for testing
            if self.anchor == RenderAnchor.CENTER:
                self.anchor = RenderAnchor.TOPLEFT
            elif self.anchor == RenderAnchor.TOPLEFT:
                self.anchor = RenderAnchor.BOTTOMCENTER
            elif self.anchor == RenderAnchor.BOTTOMCENTER:
                self.anchor = RenderAnchor.CENTER

        
        #temp
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            self.view_manager.camera.x += 1
        elif keys[pygame.K_m]:
            self.view_manager.camera.x -= 1
        


    def update(self, dt):
        #self.view_manager.camera.update(self.player1, self.player2) # simple camera follow for testing, can be expanded later for more complex behavior (like lookahead, shake, etc)
        
        self.mySprite1.update(dt)



        super().update(dt)

    



    def draw(self):
 

        self.mySprite1.draw(self.view_manager.game_surface, (32 * 4, 32 * 4), render_anchor=self.anchor, camera=self.view_manager.camera)

 

        super().draw()



    def debug_draw(self):
        self.mySprite1.debug_draw(self.view_manager.game_surface, (32 * 4, 32 * 4), render_anchor=self.anchor, camera=self.view_manager.camera)

 
        super().debug_draw()

    

