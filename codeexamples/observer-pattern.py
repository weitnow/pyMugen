from typing import Callable, Dict, List


# --- Event System (Subject) ---
class EventEmitter:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable):
        self._listeners[event_name].remove(callback)

    def emit(self, event_name: str, data=None):
        if event_name in self._listeners:
            for callback in self._listeners[event_name]:
                callback(data)


# --- Player (Subject) ---
class Player(EventEmitter):
    def __init__(self, name: str, hp: int = 100):
        super().__init__()
        self.name = name
        self.hp = hp

    def take_hit(self, damage: int):
        self.hp -= damage
        print(f"{self.name} took {damage} damage! (HP: {self.hp})")

        # Notify all systems
        self.emit("on_hit", {
            "player": self,
            "damage": damage,
            "hp": self.hp
        })

        if self.hp <= 0:
            self.emit("on_death", {"player": self})


# --- Observers (Systems) ---

class HealthBarUI:
    def on_hit(self, data):
        print(f"[UI] Update health bar: {data['hp']} HP")


class SoundSystem:
    def on_hit(self, data):
        print("[Sound] Play hit sound")

    def on_death(self, data):
        print("[Sound] Play death sound")


class ParticleSystem:
    def on_hit(self, data):
        print("[Particles] Spawn hit spark effect")


class ComboSystem:
    def on_hit(self, data):
        print(f"[Combo] Register hit for combo tracking")


# --- Setup ---
player = Player("Ryu")

ui = HealthBarUI()
sound = SoundSystem()
particles = ParticleSystem()
combo = ComboSystem()

# Subscribe systems to events
player.subscribe("on_hit", ui.on_hit)
player.subscribe("on_hit", sound.on_hit)
player.subscribe("on_hit", particles.on_hit)
player.subscribe("on_hit", combo.on_hit)

player.subscribe("on_death", sound.on_death)

# --- Simulate gameplay ---
player.take_hit(20)
player.take_hit(50)
player.take_hit(40)