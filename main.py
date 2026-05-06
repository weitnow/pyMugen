import pygame
from managers.service_provider import ServiceProvider

# --- Import all States ---
from gamestates.teststate import TestState


# --- Initialize ---
pygame.init()
display_info = pygame.display.Info()
clock = pygame.time.Clock() 

# --- Create Managers ---
sp = ServiceProvider() # create the service provider singleton to initialize all managers

#sp.graphic_manager.convert_alpha = False  # for debugging, do not convert alpha

# --- Load graphic resources ---
sp.graphic_manager.load_spritesheet("gbFighter", "assets/Graphics/Aseprite/gbFighter.png", "assets/Graphics/Aseprite/gbFighter.json") # example spritesheet with tags
sp.graphic_manager.load_spritesheet("nesFighter", "assets/Graphics/Aseprite/nesFighter.png", "assets/Graphics/Aseprite/nesFighter.json")
sp.graphic_manager.load_spritesheet("debug32", "assets/Graphics/Aseprite/debug32.png", "assets/Graphics/Aseprite/debug32.json") # example spritesheet without tags
sp.graphic_manager.load_png("debug32x32", "assets/Graphics/Aseprite/debug32x32.png") # example single PNG
sp.graphic_manager.load_spritesheet("stage", "assets/Graphics/Aseprite/stage.png", "assets/Graphics/Aseprite/stage.json")
sp.graphic_manager.load_spritesheet("gbOverlay", "assets/Graphics/Aseprite/gbOverlay.png", "assets/Graphics/Aseprite/gbOverlay.json")



# --- Set Offsets for spritesheets ---
#sp.graphic_manager.set_global_offset("gbFighter", x=0, y=0)
#sp.graphic_manager.set_global_offset("debug32x32", x=0, y=0)
#sp.graphic_manager.set_global_offset("debug32", x=0, y=0)
#sp.graphic_manager.set_tag_offset("nesFighter", "Idle", x=5, y=-3)
#sp.graphic_manager.set_frame_offset("nesFighter", 1, x=6, y=-2)

# --- Load soundeffect and music resources ---
sp.sound_manager.load_music("choices", "assets/Music/choices.mp3")
sp.sound_manager.load_music("darkchurch", "assets/Music/darkchurch.mp3")
sp.sound_manager.load_sound("jump", "assets/Soundeffects/jump3.wav")


# --- Register Game States ---
sp.gamestate_manager.add_state("test", TestState())



sp.gamestate_manager.change_state("test") # start in performance test state

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
                sp.debug_manager.debug_on = not sp.debug_manager.debug_on
            
                             

    # --- Update CORE-Systems ---
    sp.debug_manager.update(dt)
    sp.input_manager.update(dt)
    sp.view_manager.update(dt) 

    # --- Handle Input ---
    sp.gamestate_manager.handle_input()

    # --- Update current Game State ---
    sp.gamestate_manager.update(dt)

    # --- Draw ---
    sp.view_manager.clear() # clear game surface
    sp.gamestate_manager.draw() # draw to game surface

    # --- Debug Draw ---    
    if sp.debug_manager.debug_on:
        #global debug draw
        sp.debug_manager.debug_draw()      
        #gamestate specific debug draw
        sp.gamestate_manager.debug_draw()
        
    sp.view_manager.draw_to_screen()

    

pygame.quit()
