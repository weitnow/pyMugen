

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
        self.stage = GameObject((0, 0))

        self.sprite1 = Sprite().set_anim_name("gbFighter").set_frame_tag("Idle").use_camera(True)
    


    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        actions_held = self.input_manager.get_pressed_actions(0)

        if Action.RIGHT in actions_held:
            #rotate sprite
            self.sprite1.rotation += 2
            pass

        elif Action.LEFT in actions_held:
            self.sprite1.rotation -= 2
        else:
            pass
 
        if Action.UP in actions:
            self.sprite1.flip_x = not self.sprite1.flip_x

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
        self.sprite1.update(dt)

        super().update(dt)

    



    def draw(self):
        self.sprite1.draw((32, 32), RenderAnchor.TOPLEFT)

        super().draw()
      



    def debug_draw(self):
        self.sprite1.debug_draw((32, 32), RenderAnchor.TOPLEFT)

        super().debug_draw()

    

