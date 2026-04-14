

import pygame



class Particle:
    def __init__(self, pos, vel, size):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.size = size

    def update(self, dt):
        self.pos += self.vel
        self.size -= 0.1
        self.vel.y += 0.2  # gravity

    def draw(self, surface):
        pygame.draw.circle(surface, (230, 5, 76), (int(self.pos.x), int(self.pos.y)), int(self.size))

    def is_alive(self):
        return self.size > 0