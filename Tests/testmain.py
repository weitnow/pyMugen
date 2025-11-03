import pygame
import sys

# --- Initialization ---
pygame.init()

# Base (game) resolution
BASE_WIDTH, BASE_HEIGHT = 64, 64
SCALE = 8

# Create window at scaled size
screen = pygame.display.set_mode((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
pygame.display.set_caption("Move PNG Example")

clock = pygame.time.Clock()

# --- Load image ---
player_image = pygame.image.load("Assets/Graphics/Aseprite/gbFighter_test.png").convert_alpha()
pos = pygame.Vector2(16, 16)
angle = 0


# --- Create the small canvas ---
game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))


# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000.0  # delta time in seconds
    
    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Increase rotation by 45 degrees
                angle = (angle + 45) % 360

    # Rotate image
    rotated_image = pygame.transform.rotate(player_image, angle)

    # To keep it centered correctly, get its rect
    rect = rotated_image.get_rect(center=pos)


    # --- Draw to small canvas ---
    game_surface.fill((30, 30, 30))  # dark gray background
    game_surface.blit(rotated_image, rect)

    

    # --- Scale up and draw to screen ---
    scaled_surface = pygame.transform.scale(game_surface, (BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()



# --- Quit ---
pygame.quit()
sys.exit()
