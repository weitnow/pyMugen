import pygame
from graphic_manager import GraphicManager
from view_manager import ViewManager
from debug_manager import DebugManager
from input_manager import InputManager
from gamestate_manager import GameStateManager
from sound_manager import SoundManager
from gamesettings.settings_manager import SettingsManager

# --- Import all States ---
from gamestates.menustate import MenuState
from gamestates.playingstate import PlayingState
from gamestates.teststate import TestState
from gamestates.performanceteststate import PerformanceTestState

# --- Initialize ---
pygame.init()
display_info = pygame.display.Info()
clock = pygame.time.Clock() 

# --- Create Managers ---
gamestate_manager = GameStateManager()
input_manager = InputManager()
debug_manager = DebugManager()
resource_manager = GraphicManager()
resource_manager.convert_alpha = True  # for debugging, do not convert alpha
sound_manager = SoundManager()
settings_manager = SettingsManager()

# --- Create GameView and DebugView ---
view_manager = ViewManager()

# --- Load graphic resources ---
resource_manager.load_spritesheet("gbFighter", "assets/Graphics/Aseprite/gbFighter.png", "assets/Graphics/Aseprite/gbFighter.json") # example spritesheet with tags
resource_manager.load_spritesheet("nesFighter", "assets/Graphics/Aseprite/nesFighter.png", "assets/Graphics/Aseprite/nesFighter.json")
resource_manager.load_spritesheet("debug32", "assets/Graphics/Aseprite/debug32.png", "assets/Graphics/Aseprite/debug32.json", scale=4) # example spritesheet without tags
resource_manager.load_png("debug32x32", "assets/Graphics/Aseprite/debug32x32.png") # example single PNG
resource_manager.load_spritesheet("stages", "assets/Graphics/Aseprite/stages.png", "assets/Graphics/Aseprite/stages.json")


# --- Set Offsets for spritesheets ---
resource_manager.set_global_offset("nesFighter", x=0, y=0)
resource_manager.set_global_offset("debug32x32", x=0, y=0)
resource_manager.set_global_offset("debug32", x=0, y=0)
#resource_manager.set_tag_offset("nesFighter", "Idle", x=5, y=-3)
#resource_manager.set_frame_offset("nesFighter", 1, x=6, y=-2)

# --- Load soundeffect and music resources ---
sound_manager.load_music("choices", "assets/Music/choices.mp3")
sound_manager.load_music("darkchurch", "assets/Music/darkchurch.mp3")
sound_manager.load_sound("jump", "assets/Soundeffects/jump3.wav")


# --- Register Game States ---
gamestate_manager.add_state("menu", MenuState())
gamestate_manager.add_state("playing", PlayingState())
gamestate_manager.add_state("test", TestState())
gamestate_manager.add_state("performancetest", PerformanceTestState())


gamestate_manager.change_state("test") # start in performance test state

# --- Block certain events from pygame event queue to optimize ---
pygame.event.set_blocked(None) # block all events
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN]) # allow only these events


# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000.0 # dt in seconds as float (0.016 at 60fps)

    # --- Global Event Handling for all States --- 
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                debug_manager.debug_on = not debug_manager.debug_on
            
                             

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
