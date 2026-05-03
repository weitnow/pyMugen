import pygame
from decorators import singleton
from gamesettings.settings_manager import SettingsManager

@singleton
class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        # Storage
        self.music_tracks = {}   # name -> filepath
        self.sounds = {}         # name -> Sound object

        self.settings_manager = SettingsManager() # SettingsManager is a singleton
        self.settings_manager.load() 

        # Volume control
        # Load settings
        self.music_off = self.settings_manager.music_off
        self.master_volume = self.settings_manager.master_volume
        self.music_volume = self.settings_manager.music_volume
        self.sfx_volume = self.settings_manager.sfx_volume
        

        # Current state
        self.current_music = None

    # ------------------------
    # LOADING
    # ------------------------

    def load_music(self, name, path):
        self.music_tracks[name] = path

    def load_sound(self, name, path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self._get_effective_sfx_volume())
        self.sounds[name] = sound

    # ------------------------
    # MUSIC CONTROL
    # ------------------------

    def play_music(self, name, loop=True, fade_ms=0):
        if name not in self.music_tracks:
            print(f"[SoundManager] Music '{name}' not found")
            return

        if self.current_music == name:
            return  # already playing

        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)

        pygame.mixer.music.load(self.music_tracks[name])
        pygame.mixer.music.set_volume(self._get_effective_music_volume())
        pygame.mixer.music.play(-1 if loop else 0)

        self.current_music = name

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    # ------------------------
    # SOUND EFFECTS
    # ------------------------

    def play_sound(self, name):
        if name not in self.sounds:
            print(f"[SoundManager] Sound '{name}' not found")
            return

        self.sounds[name].play()

    # ------------------------
    # VOLUME CONTROL
    # ------------------------

    def set_master_volume(self, volume: float):
        self.master_volume = max(0.0, min(1.0, volume))

        # Update music
        pygame.mixer.music.set_volume(self._get_effective_music_volume())

        # Update all SFX
        for sound in self.sounds.values():
            sound.set_volume(self._get_effective_sfx_volume())

    def set_music_off(self, off: bool):
        self.music_off = off
        pygame.mixer.music.set_volume(self._get_effective_music_volume())
        if self.music_off:
            pygame.mixer.music.stop()

    def set_music_volume(self, volume: float):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float):
        self.sfx_volume = max(0.0, min(1.0, volume))

        for sound in self.sounds.values():
            sound.set_volume(self._get_effective_music_volume)


    # ------------------------
    # HELPER METHODS
    # ------------------------

    def _get_effective_music_volume(self):
        if self.music_off:
            return 0.0
        return self.master_volume * self.music_volume


    def _get_effective_sfx_volume(self):
        return self.master_volume * self.sfx_volume



    