import pygame
from ressource_manager import ResourceManager
from gameobjects.game_object import GameObject
from game_view import GameView
from debug_manager import DebugManager
from gameobjects.fighter import Fighter
from input_manager import InputManager
import globals

# --- Initialize ---
globals.fullscreen_enabled = True
pygame.init()
display_info = pygame.display.Info()
clock = pygame.time.Clock()

# --- Core Systems ---
input_manager = InputManager()
view = GameView()
resources = ResourceManager()
debug_manager = DebugManager()

# --- Load resources ---
resources.load_spritesheet("gbFighter", "assets/Graphics/Aseprite/gbFighter.png", "assets/Graphics/Aseprite/gbFighter.json")
resources.load_spritesheet("nesFighter", "assets/Graphics/Aseprite/nesFighter.png", "assets/Graphics/Aseprite/nesFighter.json")
resources.load_spritesheet("debug32", "assets/Graphics/Aseprite/debug32.png", "assets/Graphics/Aseprite/debug32.json")
resources.load_png("debug32x32", "assets/Graphics/Aseprite/debug32x32.png")

# --- Create many fighters ---
fighters = []
for i in range(1000):  # stress test count
    f = Fighter((100 + i * 10, 100), 0)
    f.get_anim("gbFighter")
    f.get_anim("nesFighter")
    f.set_anim("nesFighter")
    f.set_frame_tag("Idle")
    f.set_hurtbox(pygame.Rect(5, 10, 20, 30))
    f.set_hitbox(pygame.Rect(25, 10, 20, 15))
    fighters.append(f)



fighters[0].set_rotation(45)

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60)
    debug_manager.update_timing(dt)
    input_manager.update()

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        debug_manager.handle_input(event)

    # --- Update ---
    # each fighter gets a slightly different dt
    for i, f in enumerate(fighters):
        fake_dt = dt * (1.0 + (i * 0.002))  # each has a slight offset
        f.controller.update()
        f.update(fake_dt)

    # --- Draw ---
    view.clear()

    for f in fighters:
        f.draw(view.game_surface)
        if globals.show_hitboxes or globals.show_hurtboxes or globals.show_bounding_boxes:
            f.draw_debug(view.debug_surface, view.to_debug_coords)

    debug_manager.draw_fps(view.debug_surface)
    view.draw_to_screen()

pygame.quit()
