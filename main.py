import pygame
from resource_manager import ResourceManager
from gameobjects.game_object import GameObject
from game_view import GameView
from debug_manager import DebugManager
from gameobjects.fighter import Fighter
from input_manager import InputManager
from gamestate_manager import GameStateManager

import globals

# --- Import all States ---
from gamestates.menustate import MenuState
from gamestates.playingstate import PlayingState
from gamestates.playingstate_stresstest import PlayingStateStressTest

# --- Initialize ---
pygame.init()
display_info = pygame.display.Info()
clock = pygame.time.Clock() 

# --- Create Managers ---
game_state_manager = GameStateManager()
input_manager = InputManager()
debug_manager = DebugManager()
resource_manager = ResourceManager()

# --- Create GameView and DebugView ---
view = GameView()

# --- Load resources ---
resource_manager.load_spritesheet("gbFighter", "assets/Graphics/Aseprite/gbFighter.png", "assets/Graphics/Aseprite/gbFighter.json") # example spritesheet with tags
resource_manager.load_spritesheet("nesFighter", "assets/Graphics/Aseprite/nesFighter.png", "assets/Graphics/Aseprite/nesFighter.json") 
resource_manager.load_spritesheet("debug32", "assets/Graphics/Aseprite/debug32.png", "assets/Graphics/Aseprite/debug32.json") # example spritesheet without tags
resource_manager.load_png("debug32x32", "assets/Graphics/Aseprite/debug32x32.png") # example single PNG

# --- Register Game States ---
game_state_manager.add_state("menu", MenuState())
game_state_manager.add_state("playing", PlayingState())
game_state_manager.add_state("playing_stresstest", PlayingStateStressTest())

game_state_manager.change_state("playing_stresstest") # start in playing state








# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) # dt in milliseconds as integer (16ms at 60fps)
    # --- Update CORE-Systems ---
    debug_manager.update_timing(dt)
    input_manager.update() 
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        debug_manager.handle_input(event)


    game_state_manager.update(dt)


    view.clear()

    game_state_manager.draw()


    # Draw debug overlay
    if globals.show_hitboxes or globals.show_hurtboxes or globals.show_bounding_boxes or globals.show_fps_info:
        game_state_manager.debug_draw()
  
        globals.debug_draw = True
        globals.show_overlay = False
    else:
        globals.debug_draw = False
        globals.show_overlay = True

    debug_manager.draw_fps(view.debug_surface) # draw FPS to debug surface

    view.draw_to_screen()



  

pygame.quit()
