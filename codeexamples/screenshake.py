import pygame
import random

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# --- Game variables ---
shake_duration = 0  # frames left to shake
shake_intensity = 5  # maximum pixel offset

player_pos = [320, 240]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Press space to trigger screenshake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shake_duration = 20  # shake for 20 frames

    # --- Update ---
    if shake_duration > 0:
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        shake_duration -= 1
    else:
        offset_x, offset_y = 0, 0

    # --- Draw ---
    screen.fill((30, 30, 30))

    # Apply screenshake offset to player (or camera)
    pygame.draw.rect(screen, (200, 50, 50), 
                     (player_pos[0] - 25 + offset_x, player_pos[1] - 25 + offset_y, 50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
