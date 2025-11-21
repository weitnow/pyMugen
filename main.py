import pygame
from resource_manager import ResourceManager
from view_manager import ViewManager
from debug_manager import DebugManager
from input_manager import InputManager
from gamestate_manager import GameStateManager



# --- Import all States ---
from gamestates.menustate import MenuState
from gamestates.playingstate import PlayingState

# --- Initialize ---
pygame.init()
display_info = pygame.display.Info()
clock = pygame.time.Clock() 

# --- Create Managers ---
gamestate_manager = GameStateManager()
input_manager = InputManager()
debug_manager = DebugManager()
resource_manager = ResourceManager()

# --- Create GameView and DebugView ---
view_manager = ViewManager()

# --- Load resources ---
resource_manager.load_spritesheet("gbFighter", "assets/Graphics/Aseprite/gbFighter.png", "assets/Graphics/Aseprite/gbFighter.json") # example spritesheet with tags
resource_manager.load_spritesheet("nesFighter", "assets/Graphics/Aseprite/nesFighter.png", "assets/Graphics/Aseprite/nesFighter.json") 
resource_manager.load_spritesheet("debug32", "assets/Graphics/Aseprite/debug32.png", "assets/Graphics/Aseprite/debug32.json") # example spritesheet without tags
resource_manager.load_png("debug32x32", "assets/Graphics/Aseprite/debug32x32.png") # example single PNG

resource_manager.load_spritesheet("stages", "assets/Graphics/Aseprite/stages.png", "assets/Graphics/Aseprite/stages.json")

# --- Register Game States ---
gamestate_manager.add_state("menu", MenuState())
gamestate_manager.add_state("playing", PlayingState())

gamestate_manager.change_state("playing") # start in playing state

# --- Block certain events from pygame event queue to optimize ---
pygame.event.set_blocked(None) # block all events
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN]) # allow only these events

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) # dt in milliseconds as integer (16ms at 60fps)

    # --- Global Event Handling for all States --- 
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                debug_manager.debug_on = not debug_manager.debug_on
            elif event.key == pygame.K_F2:
                debug_manager.stop_game_for_debugging = not debug_manager.stop_game_for_debugging
            elif event.key == pygame.K_F3:
                debug_manager.view_manager.toggle_overlay()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
            view_manager.toggle_fullscreen()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
            view_manager.cycle_resolution()                         

    # --- Update CORE-Systems ---
    debug_manager.update(dt)
    input_manager.update(dt)
    view_manager.update(dt) 

    # --- Handle Input ---
    gamestate_manager.handle_input()

    # --- Update current Game State ---
    gamestate_manager.update(dt)

    # --- Draw ---
    view_manager.clear() # clear both game and debug surfaces
    gamestate_manager.draw() # draw to game surface

    # --- Debug Draw ---    
    if debug_manager.debug_on:
        #global debug draw
        debug_manager.debug_draw()      #draw to debug surface
        #gamestate specific debug draw
        gamestate_manager.debug_draw()  # draw to debug surface
        
    view_manager.draw_to_screen()

pygame.quit()
