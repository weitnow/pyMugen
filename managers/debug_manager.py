import pygame
import time
import psutil
from decorators import singleton

@singleton
class DebugManager:
    def __init__(self):
        self.debug_on = True
        self.debug_text = True
        self.DRAW_MOUSE_POS = True

        self.small_font = pygame.font.Font(None, 12)
        self.last_time = time.time()
        self.fps = 0
        self.frame_time_ms = 0
                
        self.last_system_info_update = 0
        self.system_info_update_interval = 3.0
        self.cpu_percent = 0
        self.mem_used_mb = 0
        self.process = psutil.Process()

        self._rect_cache = {} # key: (w, h, color, alpha)  #used by _get_rect_surface

        # used by begin_panel() and line()
        self._debug_cursor_x = 0
        self._debug_cursor_y = 0
        self._debug_line_height = 0
        self._in_lower_section = False

    def bind_view_manager(self, view_manager):
        self.view_manager = view_manager
        self.game_surface = view_manager.game_surface
        self.GAME_VIEW_WIDTH = view_manager.GAME_VIEW_WIDTH
        self.GAME_VIEW_HEIGHT = view_manager.GAME_VIEW_HEIGHT
        self.debug_overlay = self._get_rect_surface(self.GAME_VIEW_WIDTH, self.GAME_VIEW_HEIGHT, (0, 0, 0), 138)
        self.camera = view_manager.camera

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

        self.game_surface.blit(self.debug_overlay, (0, 0))

        self.begin_panel(8, 8)

        self.line(f"FPS: {self.fps:.1f}")
        self.line(f"CPU: {self.cpu_percent:.1f}%")
        self.line(f"RAM: {self.mem_used_mb:.1f} MB")
        self.line(f"Campos: ({self.camera.x}, {self.camera.y})")

        if self.DRAW_MOUSE_POS:
            mx, my = pygame.mouse.get_pos()
            self.line(f"Mousepos: ({mx}, {my})")

        self.line("test1")
        self.line("test2") #78

        self.line("test3fdsfadfsdfasdfafdsfasfasadsf")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")
        self.line("test3")


        
      

    def draw_debug_text(self, x=8, y=8, text="", color=(255, 255, 0)):
        if not self.debug_on or self.view_manager is None:
            return
        img = self.small_font.render(text, True, color)
        self.view_manager.game_surface.blit(img, (x, y))

    def draw_rect_overlay(self, x, y, width, height, color, alpha=128):
        surf = self._get_rect_surface(width, height, color, alpha)
        self.game_surface.blit(surf, (x, y))

    def _draw_fps_systeminfo(self, x, y):
        text = f"FPS: {self.fps:.1f} | CPU: {self.cpu_percent:.1f}% | RAM: {self.mem_used_mb:.1f} MB"
        if not self.debug_on or self.view_manager is None:
            return
        img = self.small_font.render(text, True, (255, 255, 0))
        self.view_manager.game_surface.blit(img, (x, y))

    def _update_system_info(self):
        self.cpu_percent = self.process.cpu_percent()
        mem_info = self.process.memory_info()
        self.mem_used_mb = mem_info.rss / (1024 * 1024)

    
    def _get_rect_surface(self, width, height, color, alpha):
        key = (width, height, color, alpha)

        if key not in self._rect_cache:
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            surf.fill((*color, alpha))
            self._rect_cache[key] = surf

        return self._rect_cache[key]
    
    def begin_panel(
        self,
        x=8,
        y=8,
        line_height=None,

        upper_section_max_y=78,
        lower_section_min_y=420,

        column_width=150,
        max_columns=6
    ):
        self.debug_start_x = x
        self.debug_start_y = y

        self._debug_cursor_x = x
        self._debug_cursor_y = y

        self.upper_section_max_y = upper_section_max_y
        self.lower_section_min_y = lower_section_min_y

        self.debug_column_width = column_width
        self.debug_max_columns = max_columns

        self.current_column = 0

        self._in_lower_section = False

        if line_height is None:
            line_height = self.small_font.get_height() + 2

        self._debug_line_height = line_height

    def line(self, text="", color=(255, 255, 0)):

        self.draw_debug_text(
            x=self._debug_cursor_x,
            y=self._debug_cursor_y,
            text=text,
            color=color
        )

        self._debug_cursor_y += self._debug_line_height

        # =========================
        # UPPER SECTION
        # =========================

        if not self._in_lower_section:

            if self._debug_cursor_y >= self.upper_section_max_y:

                # still allowed to create columns
                if self.current_column < self.debug_max_columns - 1:
                    self.current_column += 1
                    self._debug_cursor_x += self.debug_column_width
                    self._debug_cursor_y = self.debug_start_y

                # switch to lower section
                else:
                    self._in_lower_section = True
                    self._debug_cursor_x = 8

        # =========================
        # LOWER SECTION
        # =========================

        else:

            if self._debug_cursor_y >= self.lower_section_min_y:

                self.current_column += 1
                self._debug_cursor_x += self.debug_column_width
                self._debug_cursor_y = self.lower_section_min_y
    
    
    