import pygame

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

# --- Player variables ---
player_pos = pygame.Vector2(200, 250)
player_vel = pygame.Vector2(0, 0)
player_size = (30, 50)

# --- Physics ---
gravity = 2000         # pixels/sec², strong gravity for snappy fall
jump_velocity = -600   # initial jump velocity, fast upward
ground_y = 250
on_ground = True

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        player_vel.y = jump_velocity
        on_ground = False

    # --- Variable jump height ---
    # If player releases jump early, reduce upward speed
    #if not keys[pygame.K_SPACE] and player_vel.y < 0:
    #    player_vel.y += gravity * dt * 1.5  # shortens the jump

    # --- Physics ---
    player_vel.y += gravity * dt
    player_pos.y += player_vel.y * dt

    # --- Ground collision ---
    if player_pos.y >= ground_y:
        player_pos.y = ground_y
        player_vel.y = 0
        on_ground = True

    # --- Draw ---
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (200, 50, 50), (*player_pos, *player_size))
    pygame.draw.line(screen, (255, 255, 255), (0, ground_y + player_size[1]), (400, ground_y + player_size[1]), 2)

    pygame.display.flip()

pygame.quit()
