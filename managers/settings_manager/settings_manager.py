import json
import os

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.folder = "gamesettings"

        # Default settings
        self.music_off = False
        self.master_volume = 1.0
        self.music_volume = 1.0
        self.sfx_volume = 1.0
        self.resolution = (800, 600)
        self.fullscreen = False

    def load(self):
        """Load settings from file."""
        if not os.path.exists(os.path.join(self.folder, self.filename)):
            print("Settings file not found. Using defaults.")
            return

        with open(os.path.join(self.folder, self.filename), "r") as f:
            data = json.load(f)

        self.music_off = data.get("music_off", self.music_off)
        self.master_volume = data.get("master_volume", self.master_volume)
        self.music_volume = data.get("music_volume", self.music_volume)
        self.sfx_volume = data.get("sfx_volume", self.sfx_volume)
        self.resolution = tuple(data.get("resolution", self.resolution))
        self.fullscreen = data.get("fullscreen", self.fullscreen)

        print("Settings loaded.")

    def save(self):
        """Save settings to file."""
        data = {
            "music_off": self.music_off,
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "resolution": list(self.resolution),  # JSON needs list, not tuple
            "fullscreen": self.fullscreen
        }

        with open(os.path.join(self.folder, self.filename), "w") as f:
            json.dump(data, f, indent=4)

        print("Settings saved.")


if __name__ == "__main__":
    settings = SettingsManager()
    settings.load()

    # Modify settings as needed
    settings.music_off = True
    settings.master_volume = 0.8
    settings.music_volume = 0.8
    settings.sfx_volume = 0.8
    settings.resolution = (1024, 768)
    settings.fullscreen = True

    settings.save()