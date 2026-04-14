import random
from particle import Particle



class ParticleManager:
    def __init__(self):
        self.particles = []

    def emit(self, pos):
        vel = [random.randint(0, 20) / 10 - 1, -2]
        size = random.randint(1, 3)
        self.particles.append(Particle(pos, vel, size))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)

        # clean dead particles (SAFE way)
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)