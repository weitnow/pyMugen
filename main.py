import pygame
from ressourcemanager import ResourceManager
from gameobject import GameObject

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Load all resources
resources = ResourceManager() 
resources.load_spritesheet("gbFighter", "Assets/Graphics/Aseprite/gbFighter.png", "Assets/Graphics/Aseprite/gbFighter.json")


# Create GameObjects using resource names only
player = GameObject("gbFighter", pygame.Vector2(100, 100))


player.set_frame_tag("Idle")


running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(dt)


    screen.fill((0, 0, 0))
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
