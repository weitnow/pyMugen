import json
import os

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.folder = "gamesettings"

        # Default settings
        self.music_volume = 1.0
        self.soundeffects_volume = 1.0
        self.resolution = (800, 600)
        self.fullscreen = False

    def load(self):
        """Load settings from file."""
        if not os.path.exists(os.path.join(self.folder, self.filename)):
            print("Settings file not found. Using defaults.")
            return

        with open(os.path.join(self.folder, self.filename), "r") as f:
            data = json.load(f)

        self.music_volume = data.get("music_volume", self.music_volume)
        self.soundeffects_volume = data.get("soundeffects_volume", self.soundeffects_volume)
        self.resolution = tuple(data.get("resolution", self.resolution))
        self.fullscreen = data.get("fullscreen", self.fullscreen)

        print("Settings loaded.")

    def save(self):
        """Save settings to file."""
        data = {
            "music_volume": self.music_volume,
            "soundeffects_volume": self.soundeffects_volume,
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
    settings.music_volume = 0.8
    settings.soundeffects_volume = 0.8
    settings.resolution = (1024, 768)
    settings.fullscreen = True

    settings.save()