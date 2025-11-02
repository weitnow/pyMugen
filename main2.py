import pygame
from ressourcemanager import ResourceManager
from gameobject import GameObject
from gameview import GameView

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
resources = ResourceManager()

resources.load_spritesheet("gbFighter", "Assets/Graphics/Aseprite/gbFighter.png", "Assets/Graphics/Aseprite/gbFighter.json")
resources.load_spritesheet("nesFighter", "Assets/Graphics/Aseprite/nesFighter.png", "Assets/Graphics/Aseprite/nesFighter.json")

view = GameView()
player = GameObject((100, 100))
player.get_anim("gbFighter")
player.set_anim("gbFighter")
player.set_frame_tag("Idle")
player.set_hurtbox(pygame.Rect(5, 10, 20, 30))
player.set_hitbox(pygame.Rect(25, 10, 20, 15))

enemy = GameObject((160, 100))
enemy.get_anim("nesFighter")
enemy.set_anim("nesFighter")
enemy.set_frame_tag("Idle")
enemy.set_hurtbox(pygame.Rect(6, 8, 20, 28))
enemy.set_hitbox(pygame.Rect(22, 8, 20, 14))

running = True
while running:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_F1:
                view.debug_draw = not view.debug_draw

    player.update(dt)
    enemy.update(dt)

    view.clear()
    player.draw(view.game_surface)
    enemy.draw(view.game_surface)

    if view.debug_draw:
        player.draw_debug(view.debug_surface, view.to_debug_coords)
        enemy.draw_debug(view.debug_surface, view.to_debug_coords)

    view.draw_to_screen()

pygame.quit()
