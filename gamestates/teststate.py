

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
        pass


    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        actions_held = self.input_manager.get_pressed_actions(0)

        if Action.RIGHT in actions_held:
            #rotate sprite
            pass

        elif Action.LEFT in actions_held:
            pass
        else:
            pass
 
        if Action.UP in actions:
            pass

        if Action.DOWN in actions:
            # cycle through anchors for testing
            if self.anchor == RenderAnchor.CENTER:
                pass
            elif self.anchor == RenderAnchor.TOPLEFT:
                pass
            elif self.anchor == RenderAnchor.BOTTOMCENTER:
                pass

        
        #temp
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            self.view_manager.camera.x += 1
        elif keys[pygame.K_m]:
            self.view_manager.camera.x -= 1
        


    def update(self, dt):
        #self.view_manager.camera.update(self.player1, self.player2) # simple camera follow for testing, can be expanded later for more complex behavior (like lookahead, shake, etc)
        super().update(dt)

    



    def draw(self):
        super().draw()



    def debug_draw(self):
        super().debug_draw()

    

