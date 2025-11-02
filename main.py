import pygame
from ressourcemanager import ResourceManager
from gameobject import GameObject
from gameview import GameView
from debugmanager import DebugManager
import globals

# --- Initialize ---
pygame.init()
display_info = pygame.display.Info()
clock = pygame.time.Clock()

# --- Create GameView and DebugView ---
view = GameView()

# --- Load resources ---
resources = ResourceManager()
resources.load_spritesheet("gbFighter", "Assets/Graphics/Aseprite/gbFighter.png", "Assets/Graphics/Aseprite/gbFighter.json") # example spritesheet with tags
resources.load_spritesheet("nesFighter", "Assets/Graphics/Aseprite/nesFighter.png", "Assets/Graphics/Aseprite/nesFighter.json") 
resources.load_spritesheet("debug32", "Assets/Graphics/Aseprite/debug32.png", "Assets/Graphics/Aseprite/debug32.json") # example spritesheet without tags
resources.load_png("debug32x32", "Assets/Graphics/Aseprite/debug32x32.png") # example single PNG

# --- Create DebugManager ---
debug_manager = DebugManager()


# --- Create objects ---
player = GameObject((100, 100))
player.origin_center_bottom = True
player.get_anim("gbFighter")
player.get_anim("nesFighter")
player.set_anim("nesFighter")
player.set_frame_tag("Idle")

player.set_hurtbox(pygame.Rect(5, 10, 20, 30))
player.set_hitbox(pygame.Rect(25, 10, 20, 15))

enemy = GameObject((150, 100))
enemy.origin_center_bottom = True
enemy.get_anim("gbFighter")
enemy.set_anim("gbFighter")
enemy.set_frame_tag("Idle")
enemy.set_hurtbox(pygame.Rect(6, 8, 20, 28))
enemy.set_hitbox(pygame.Rect(22, 8, 20, 14))

debugbox_asprite = GameObject((10, 10))
debugbox_asprite.get_anim("debug32")
debugbox_asprite.set_anim("debug32")
debugbox_asprite.set_frame(1) # second frame of spritesheet

debugbox = GameObject((50, 50))
debugbox.get_anim("debug32x32")
debugbox.set_anim("debug32x32")
debugbox.set_frame(0) # has only one frame



# --- Aspect ratio scaler ---
def blit_scaled_center(source, target):
    """Scale source surface to fit target while keeping aspect ratio and black bars"""
    sw, sh = source.get_size()
    tw, th = target.get_size()

    scale = min(tw / sw, th / sh)
    new_size = (int(sw * scale), int(sh * scale))
    scaled = pygame.transform.scale(source, new_size)

    x = (tw - new_size[0]) // 2
    y = (th - new_size[1]) // 2

    target.fill((0, 0, 0))
    target.blit(scaled, (x, y))

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60)
    # --- Update CORE-Systems ---
    debug_manager.update_timing(dt)
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        debug_manager.handle_input(event)

    # --- Update ---
    player.update(dt)
    enemy.update(dt)
    debugbox_asprite.update(dt)
    debugbox.update(dt)

    view.clear()
    player.draw(view.game_surface)
    enemy.draw(view.game_surface)
    debugbox_asprite.draw(view.game_surface)
    debugbox.draw(view.game_surface)

    # Draw debug overlay
    if globals.show_hitboxes or globals.show_hurtboxes or globals.show_bounding_boxes or globals.show_fps_info:
        player.draw_debug(view.debug_surface, view.to_debug_coords)
        enemy.draw_debug(view.debug_surface, view.to_debug_coords)
        debugbox_asprite.draw_debug(view.debug_surface, view.to_debug_coords)
        debugbox.draw_debug(view.debug_surface, view.to_debug_coords)
        globals.debug_draw = True
        globals.show_overlay = False
    else:
        globals.debug_draw = False
        globals.show_overlay = True

    debug_manager.draw_fps(view.debug_surface) # draw directly to final screen

    view.draw_to_screen()



  

pygame.quit()
