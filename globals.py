# --- Configuration ---
GAME_RES = (209, 155)
DEBUG_SCALE = 8 # scale factor for debug view

# overlay transparent area (x, y, width, height)
OVERLAY_VIEWPORT = (145, 25, 209, 155)      

# --- Gameview Settings ---
available_resolutions = [
    (640, 360),
    (960, 540),
    (1280, 720),
    (1920, 1080)
]
current_resolution_index = 3  # start with 1920x1080
fullscreen_enabled = False
