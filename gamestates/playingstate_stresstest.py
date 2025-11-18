import pygame
from gamestates.gamestate_base import GameState
from gameobjects.fighter import Fighter


class PlayingStateStressTest(GameState):

    def enter(self):
        # Create 200 fighter instances spaced by 20px in X
        self.players = []
        base_x = 50
        base_y = 100
        spacing = 20
        count = 1000

        for i in range(count):
            x = base_x + i * spacing
            p = Fighter((x, base_y), 0)
            p.get_anim("gbFighter")
            p.get_anim("nesFighter")
            p.set_anim("nesFighter")
            p.set_frame_tag("Idle")
            p.set_hurtbox(pygame.Rect(5, 10, 20, 30))
            p.set_hitbox(pygame.Rect(25, 10, 20, 15))
            self.players.append(p)

    def exit(self):
        self.players.clear()

    def update(self, dt):
        # update controllers (if any) and physics/animations
        for p in self.players:
            # ensure controllers are advanced if they're present
            try:
                p.controller.update()
            except Exception:
                pass
            p.update(dt)

    def draw(self):
        for p in self.players:
            p.draw(self.view.game_surface)

    def debug_draw(self):
        for p in self.players:
            p.draw_debug(self.view.debug_surface, self.view.to_debug_coords)
