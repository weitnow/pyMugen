import pygame
import random
import sys
import psutil  # NEW

# --- CONFIG ---
INTERNAL_WIDTH = 640
INTERNAL_HEIGHT = 480
NUM_OBJECTS = 2000

pygame.init()

screen = pygame.display.set_mode(
    (INTERNAL_WIDTH, INTERNAL_HEIGHT),
    pygame.SCALED | pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
)

pygame.display.set_caption("RenderTarget Stress Test")

clock = pygame.time.Clock()

render_target = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT)).convert()

# --- CPU tracking ---
process = psutil.Process()
cpu_usage = 0

class Particle:
    def __init__(self):
        self.x = random.uniform(0, INTERNAL_WIDTH)
        self.y = random.uniform(0, INTERNAL_HEIGHT)
        self.vx = random.uniform(-100, 100)
        self.vy = random.uniform(-100, 100)
        self.size = random.randint(2, 5)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x < 0 or self.x > INTERNAL_WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > INTERNAL_HEIGHT:
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.size, self.size))


particles = [Particle() for _ in range(NUM_OBJECTS)]

frame_counter = 0

while True:
    dt = clock.tick(60) / 1000.0
    frame_counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- UPDATE ---
    for p in particles:
        p.update(dt)

    # --- DRAW ---
    render_target.fill((10, 10, 20))

    for p in particles:
        p.draw(render_target)

    screen.blit(render_target, (0, 0))
    pygame.display.flip()

    # --- CPU measurement (update every ~0.5 sec for stability) ---
    if frame_counter % 30 == 0:
        cpu_usage = process.cpu_percent(interval=None)

    # --- DEBUG ---
    pygame.display.set_caption(
        f"FPS: {clock.get_fps():.1f} | Objects: {NUM_OBJECTS} | CPU: {cpu_usage:.1f}%"
    )