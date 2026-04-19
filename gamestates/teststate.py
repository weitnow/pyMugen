

from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import PlayerController, Action
from gameobjects.sprite import Sprite
from physics_components import FighterPhysicsComponent
import pygame

from gameobjects.sprite import RenderAnchor



class TestState(GameState):

    def enter(self):
        #create a game object and add sprite
        self.mySprite1 = Sprite().set_anim_name("debug32")
        self.mySprite1.set_frame(0)

        self.myGameObject = GameObject(pos=(128,32), render_anchor=RenderAnchor.CENTER)
        self.myGameObject.add_sprite(Sprite().set_anim_name("debug32").set_frame(1))
        self.myGameObject.add_camera(self.view_manager.camera)


        self.randoranchor = RenderAnchor.CENTER

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)

        if Action.RIGHT in actions:
            self.myGameObject.pos.x += 10

        elif Action.LEFT in actions:
            self.myGameObject.pos.x -= 10
 
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

        
        #temp
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            self.view_manager.camera.x += 1
        elif keys[pygame.K_m]:
            self.view_manager.camera.x -= 1
        


    def update(self, dt):
        #self.view_manager.camera.update(self.player1, self.player2) # simple camera follow for testing, can be expanded later for more complex behavior (like lookahead, shake, etc)
        
        self.mySprite1.update(dt)

        self.myGameObject.update(dt)


        super().update(dt)

    



    def draw(self):
        self.mySprite1.draw(self.view_manager.game_surface, (32, 32), render_anchor=self.randoranchor, camera=self.view_manager.camera)

        self.myGameObject.draw(self.view_manager.game_surface)
 

        super().draw()



    def debug_draw(self):
        self.mySprite1.debug_draw(self.view_manager.debug_surface, (32, 32), render_anchor=self.randoranchor, camera=self.view_manager.camera)

        #self.myGameObject.debug_draw(self.view_manager.debug_surface)
 
        super().debug_draw()

    

