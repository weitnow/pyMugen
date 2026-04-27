import pygame
import time
import psutil
from decorators import singleton

@singleton
class DebugManager:
    def __init__(self):
        self.debug_on = True
        self.debug_text = True


        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 12)
        self.last_time = time.time()
        self.fps = 0
        self.frame_time_ms = 0
        self.view_manager = None
                
        self.last_system_info_update = 0
        self.system_info_update_interval = 3.0
        self.cpu_percent = 0
        self.mem_used_mb = 0
        self.process = psutil.Process()

    def set_view_manager(self, view_manager):
        self.view_manager = view_manager

    def update(self, dt):
        if not self.debug_on:
            return
        now = time.time()
        self.frame_time_ms = dt * 1000.0
        self.fps = 1.0 / dt if dt > 0 else 0
        self.last_time = now
        if now - self.last_system_info_update >= self.system_info_update_interval:
            self._update_system_info()
            self.last_system_info_update = now

    def debug_draw(self):
        if not self.debug_on:
            return
        self._draw_fps_systeminfo()

    def draw_debug_text(self, x=8, y=8, text="", color=(255, 255, 0)):
        if not self.debug_on or self.view_manager is None:
            return
        img = self.small_font.render(text, True, color)
        self.view_manager.game_surface.blit(img, (x, y))

    def _draw_fps_systeminfo(self):
        text = f"FPS: {self.fps:.1f} | CPU: {self.cpu_percent:.1f}% | RAM: {self.mem_used_mb:.1f} MB"
        if not self.debug_on or self.view_manager is None:
            return
        img = self.small_font.render(text, True, (255, 255, 0))
        self.view_manager.game_surface.blit(img, (8, 8))

    def _update_system_info(self):
        self.cpu_percent = self.process.cpu_percent()
        mem_info = self.process.memory_info()
        self.mem_used_mb = mem_info.rss / (1024 * 1024)

    