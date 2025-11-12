import pygame
import numpy as np

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# --- Object parameters ---
num_objects = 1000
player_size = np.array([30, 50])

positions = np.zeros((num_objects, 2))
positions[:, 0] = np.random.uniform(0, screen.get_width() - player_size[0], num_objects)
positions[:, 1] = 250

velocities = np.zeros((num_objects, 2))
on_ground = np.ones(num_objects, dtype=bool)

gravity = 2000
jump_velocity = -600
ground_y = 250

# --- Jump offsets (phase) ---
# Each object will jump after a small delay
jump_offsets = np.linspace(0, 0.5, num_objects)  # 0 to 0.5 seconds
jumped = np.zeros(num_objects, dtype=bool)       # track which objects have jumped this cycle

# Global timer
time_elapsed = 0

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000
    time_elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input ---
    keys = pygame.key.get_pressed()
    space_pressed = keys[pygame.K_SPACE]

    # --- Jump with offsets ---
    if space_pressed:
        to_jump = (time_elapsed >= jump_offsets) & on_ground & (~jumped)
        velocities[to_jump, 1] = jump_velocity
        on_ground[to_jump] = False
        jumped[to_jump] = True

    # Reset jumped flag when all objects landed
    if np.all(on_ground):
        jumped[:] = False
        time_elapsed = 0  # restart jump cycle

    # --- Physics ---
    velocities[:, 1] += gravity * dt
    positions += velocities * dt

    # Ground collision
    hit_ground = positions[:, 1] >= ground_y
    positions[hit_ground, 1] = ground_y
    velocities[hit_ground, 1] = 0
    on_ground[hit_ground] = True

    # --- Draw ---
    screen.fill((30, 30, 30))
    for pos in positions:
        pygame.draw.rect(screen, (200, 50, 50), (*pos, *player_size))
    pygame.draw.line(screen, (255, 255, 255),
                     (0, ground_y + player_size[1]),
                     (screen.get_width(), ground_y + player_size[1]), 2)

    pygame.display.flip()

pygame.quit()
