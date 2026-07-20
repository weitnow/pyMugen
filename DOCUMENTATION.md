# pyMugen – Code Documentation

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Directory Structure](#2-directory-structure)
3. [Architecture Overview](#3-architecture-overview)
4. [Entry Point – `main.py`](#4-entry-point--mainpy)
5. [Managers](#5-managers)
   - [ServiceProvider](#51-serviceprovider)
   - [GameStateManager](#52-gamestatemanager)
   - [GraphicManager & AnimationData](#53-graphicmanager--animationdata)
   - [InputManager](#54-inputmanager)
   - [ViewManager & Camera](#55-viewmanager--camera)
   - [SoundManager](#56-soundmanager)
   - [SettingsManager](#57-settingsmanager)
   - [DebugManager](#58-debugmanager)
   - [EventManager](#59-eventmanager)
   - [ParticleManager](#510-particlemanager)
6. [Game Objects](#6-game-objects)
   - [Sprite](#61-sprite)
   - [GameObject](#62-gameobject)
   - [BaseFighter](#63-basefighter)
7. [Components](#7-components)
   - [PhysicsComponent / FighterPhysicsComponent](#71-physicscomponent--fighterphysicscomponent)
   - [PlayerController](#72-playercontroller)
8. [Game States](#8-game-states)
   - [GameState (abstract base)](#81-gamestate-abstract-base)
   - [TestState](#82-teststate)
9. [Stages](#9-stages)
   - [BaseStage](#91-basestage)
   - [Stage1](#92-stage1)
10. [Utilities](#10-utilities)
    - [globals.py](#101-globalspy)
    - [decorators.py](#102-decoratorspy)
11. [How-To Guides](#11-how-to-guides)
    - [Add a new Game State](#111-add-a-new-game-state)
    - [Create a new Fighter](#112-create-a-new-fighter)
    - [Load and play a sprite animation](#113-load-and-play-a-sprite-animation)
    - [Add a new Stage](#114-add-a-new-stage)

---

## 1. Project Overview

**pyMugen** is a 2D fighting-game engine prototype built with **Python + pygame**. It follows a classic game-loop architecture with:

- A central **ServiceProvider** that holds all manager singletons.
- A **GameStateManager** to switch between scenes/states (menus, gameplay, …).
- A **Component-based** entity model (`Sprite → GameObject → BaseFighter`).
- Aseprite-based **spritesheet** support with tag-based animations, per-frame offsets, and rotation/flip caching.
- A **Camera** with smooth follow, world-clamping, and screenshake (trauma system).
- **Keyboard + gamepad** input abstraction with a special-move input buffer.

---

## 2. Directory Structure

```
pyMugen/
├── main.py                          # Entry point and main loop
├── globals.py                       # Global color constants
├── decorators.py                    # @singleton decorator
├── managers/
│   ├── service_provider.py          # Creates and wires all managers
│   ├── gamestate_manager.py
│   ├── graphic_manager.py           # Loads spritesheets / PNGs, caches transforms
│   ├── input_manager.py             # Keyboard + gamepad → Action enum
│   ├── view_manager/
│   │   ├── view_manager.py          # Screen / game surface, drawing helpers
│   │   └── camera.py               # Camera follow + screenshake
│   ├── sound_manager.py             # Music + SFX playback
│   ├── settings_manager/
│   │   ├── settings_manager.py      # Load/save JSON settings
│   │   └── settings.json
│   ├── debug_manager.py             # FPS overlay, debug text/rects
│   ├── event_manager.py             # Observer-pattern event bus
│   └── particle_manager/
│       ├── particle_manager.py
│       └── particle.py
├── gameobjects/
│   ├── sprite.py                    # Animated sprite base
│   ├── game_object.py               # Sprite + world position + hitboxes
│   ├── base_fighter.py              # Fighter entity (extends GameObject)
│   └── components/
│       ├── physics_components.py    # Gravity / jump / walk physics
│       └── player_controller_component.py  # Input → actions + special moves
├── gamestates/
│   ├── gamestate.py                 # Abstract base class for all states
│   └── teststate.py                 # Example gameplay state
├── stages/
│   ├── base_stage.py                # Abstract base class for stages
│   └── stage1.py                    # Example stage
├── assets/                          # Graphics, music, sound effects
└── codeexamples/                    # Standalone feature demos
```

---

## 3. Architecture Overview

```
main.py
  └─ ServiceProvider (singleton)
        ├─ GameStateManager   ← manages active GameState
        ├─ GraphicManager     ← holds all AnimationData (frames, tags, offsets)
        ├─ InputManager       ← maps keys/buttons to Action enum
        ├─ ViewManager        ← screen, game_surface, Camera
        ├─ SoundManager       ← music + SFX
        ├─ SettingsManager    ← persisted JSON settings
        └─ DebugManager       ← FPS/overlay/debug text

GameState  (abstract)
  ├─ player1, player2 : BaseFighter
  ├─ stage            : BaseStage
  └─ game_objects     : list[GameObject]

GameObject (Sprite + world position)
  ├─ physics : PhysicsComponent
  └─ hitboxes / hurtboxes

BaseFighter (GameObject)
  └─ player_controller : PlayerController
```

Every manager is a **singleton** (see `@singleton` in `decorators.py`). Acquiring a manager from anywhere is as simple as calling its constructor – you always get the same instance.

---

## 4. Entry Point – `main.py`

`main.py` is the only script you run directly. It:

1. Initialises pygame and creates the `ServiceProvider`.
2. **Loads all assets** (spritesheets, PNGs, music, SFX).
3. **Registers game states** and immediately switches to one.
4. Runs the **main loop** at 60 fps:

```
while running:
    dt = clock.tick(60) / 1000          # seconds since last frame

    # Core systems
    sp.debug_manager.update(dt)
    sp.input_manager.update(dt)
    sp.view_manager.update(dt)

    # State
    sp.gamestate_manager.handle_input()
    sp.gamestate_manager.update(dt)

    # Render
    sp.view_manager.clear()
    sp.gamestate_manager.draw()
    sp.view_manager.draw_to_screen()
```

**Important**: `pygame.K_ESCAPE` / window close exits the loop; `pygame.K_F1` toggles the debug overlay.

---

## 5. Managers

### 5.1 ServiceProvider

**File**: `managers/service_provider.py`

The single point of truth for all managers.

```python
from managers.service_provider import ServiceProvider
sp = ServiceProvider()   # always returns the one instance

sp.graphic_manager
sp.view_manager
sp.input_manager
sp.gamestate_manager
sp.sound_manager
sp.settings_manager
sp.debug_manager
```

`DebugManager` and `ViewManager` receive a back-reference via `bind_service_provider(sp)` because they depend on each other at startup.

---

### 5.2 GameStateManager

**File**: `managers/gamestate_manager.py`  
**Singleton**: yes

Manages a dictionary of named `GameState` objects and one active state.

| Method | Description |
|---|---|
| `add_state(name, state)` | Register a state under a string key. |
| `change_state(name)` | Exit the current state and enter the named one. |
| `handle_input()` | Delegates to `current_state.handle_input()`. |
| `update(dt)` | Delegates to `current_state.update(dt)`. |
| `draw()` | Delegates to `current_state.draw()`. |
| `debug_draw()` | Delegates to `current_state.debug_draw()`. |

**Example**:

```python
from managers.service_provider import ServiceProvider
from gamestates.teststate import TestState

sp = ServiceProvider()
sp.gamestate_manager.add_state("gameplay", TestState())
sp.gamestate_manager.change_state("gameplay")
```

---

### 5.3 GraphicManager & AnimationData

**File**: `managers/graphic_manager.py`  
**Singleton**: `GraphicManager` is a singleton; `AnimationData` is a plain data class.

#### GraphicManager

Loads Aseprite spritesheets (PNG + JSON export) and single PNG images, and caches all transformed (rotated/flipped) frames.

| Method | Description |
|---|---|
| `load_spritesheet(name, image_path, json_path, scale=1)` | Parse an Aseprite JSON export and store all frames and tags. |
| `load_png(name, image_path, scale=1)` | Load a single static image. |
| `get_animationdata_reference(name, scale)` | Return the `AnimationData` object (read-only reference). |
| `get_or_create_scaled(name, scale)` | Ensure a scaled variant exists; creates it from scale=1 if absent. |
| `get_rotated_frame(anim_name, frame_idx, angle, flip_x, flip_y, scale)` | Return a cached transformed frame surface. |
| `set_global_offset(base_name, x, y, scale)` | Shift all frames of an animation. |
| `set_tag_offset(base_name, tag_name, x, y, scale)` | Shift all frames within a tag. |
| `set_frame_offset(base_name, frame_idx, x, y, scale)` | Shift one specific frame. |

**Example**:

```python
sp.graphic_manager.load_spritesheet(
    "hero",
    "assets/Graphics/hero.png",
    "assets/Graphics/hero.json"
)
# optional fine-tuning:
sp.graphic_manager.set_tag_offset("hero", "Idle", x=2, y=-1, scale=1)
```

#### AnimationData

Stores the data for one spritesheet / PNG at one scale level.

| Attribute | Type | Description |
|---|---|---|
| `base_name` | `str` | Key used in `GraphicManager.animations`. |
| `frames` | `dict[int, Surface]` | Frame index → pygame Surface. |
| `durations` | `dict[int, int]` | Frame index → duration in ms. |
| `tags` | `dict[str, dict]` | Tag name → `{"from": int, "to": int, …}`. |
| `sprite_size` | `tuple` | `(width, height)` of a single frame at this scale. |
| `png` | `bool` | `True` if this is a static PNG (single frame). |
| `scale` | `int` | Scale factor relative to the source image. |
| `final_offsets` | `dict[int, (x,y)]` | Pre-computed draw offsets per frame. |

---

### 5.4 InputManager

**File**: `managers/input_manager.py`  
**Singleton**: yes

Abstracts keyboard and gamepad input for up to **2 players** into an `Action` enum.

#### Action Enum

```
RIGHT, LEFT, DOWN, UP, A, B, START
DOWN_RIGHT, DOWN_LEFT, UP_RIGHT, UP_LEFT   (diagonals)
```

#### Key methods

| Method | Description |
|---|---|
| `update(dt)` | Snapshot current pressed state. Call once per frame. |
| `get_pressed_actions(player_index)` | `set[Action]` of everything held this frame. |
| `get_just_pressed_actions(player_index)` | `set[Action]` of keys pressed *this* frame (not previous). |

**Default key mapping**:

| Player | LEFT | RIGHT | UP | DOWN | A | B | START |
|---|---|---|---|---|---|---|---|
| P1 | A | D | W | S | Z | U | Enter |
| P2 | ← | → | ↑ | ↓ | Num1 | Num2 | NumEnter |

**Example**:

```python
from managers.input_manager import InputManager, Action

im = InputManager()
if Action.RIGHT in im.get_pressed_actions(0):
    player.move_right()
```

---

### 5.5 ViewManager & Camera

#### ViewManager

**File**: `managers/view_manager/view_manager.py`  
**Singleton**: yes

Owns the pygame **screen** and an internal `game_surface` that everything is drawn onto. Provides primitive drawing helpers.

| Attribute | Value | Description |
|---|---|---|
| `GAME_WINDOW_WIDTH` | 960 | Logical game width in pixels. |
| `GAME_WINDOW_HEIGHT` | 540 | Logical game height in pixels. |
| `VIEW_LEFT_BOUND` | 94 | Left edge of the visible stage area. |
| `VIEW_RIGHT_BOUND` | 868 | Right edge of the visible stage area. |
| `VIEW_TOP_BOUND` | 86 | Top edge of the visible stage area. |
| `VIEW_BOTTOM_BOUND` | 454 | Bottom edge of the visible stage area. |
| `camera` | `Camera` | The active camera instance. |
| `game_surface` | `pygame.Surface` | Surface that all game objects draw onto. |

| Method | Description |
|---|---|
| `clear()` | Fill `game_surface` with the clear colour. |
| `draw_to_screen()` | Blit `game_surface` to the screen and call `pygame.display.flip()`. |
| `draw_rect(x, y, w, h, color)` | Draw a filled rectangle. |
| `draw_rect_outline(x, y, w, h, color, thickness=1)` | Draw a rectangle outline. |
| `draw_circle(x, y, radius, color)` | Draw a filled circle. |
| `draw_circle_outline(x, y, radius, color, thickness=1)` | Draw a circle outline. |

#### Camera

**File**: `managers/view_manager/camera.py`

Follows the midpoint between two players, clamps to world bounds, and supports trauma-based screenshake.

| Attribute | Description |
|---|---|
| `x`, `y` | Camera offset (pixels). Auto-clamped when `clamp_to_world` is `True`. |
| `smooth_speed` | Lerp factor per frame (0.0–1.0). Default `0.12`. |
| `follow_enabled` | Toggle camera following. |
| `clamp_to_world` | Prevent the camera from showing areas outside the stage. |
| `world_width/height` | Set by the stage via `configure_camera()`. |

| Method | Description |
|---|---|
| `update(dt, p1, p2)` | Advance follow and screenshake. Pass the two player objects. |
| `apply_vec2(pos, shake_factor=1.0)` | Convert a world position to a screen position. |
| `add_trauma(amount)` | Add screenshake (0.0–1.0, stacks). |

**Example**:

```python
camera = sp.view_manager.camera
screen_pos = camera.apply_vec2(player.world_pos)
camera.add_trauma(0.6)   # big hit screenshake
```

---

### 5.6 SoundManager

**File**: `managers/sound_manager.py`  
**Singleton**: yes

| Method | Description |
|---|---|
| `load_music(name, path)` | Register a music file under a key. |
| `load_sound(name, path)` | Load a WAV/OGG sound effect. |
| `play_music(name, loop=True, fade_ms=0)` | Start or switch music. |
| `stop_music()` | Stop playback. |
| `pause_music()` / `resume_music()` | Pause / resume. |
| `play_sound(name)` | Play a one-shot sound effect. |
| `set_master_volume(volume)` | Float 0.0–1.0; updates music + all SFX. |
| `set_music_volume(volume)` | Float 0.0–1.0. |
| `set_sfx_volume(volume)` | Float 0.0–1.0. |
| `set_music_off(off)` | Mute/unmute music entirely. |

**Example**:

```python
sp.sound_manager.play_music("darkchurch", loop=True, fade_ms=500)
sp.sound_manager.play_sound("jump")
```

---

### 5.7 SettingsManager

**File**: `managers/settings_manager/settings_manager.py`

Persists user preferences to `gamesettings/settings.json`.

| Attribute | Default | Description |
|---|---|---|
| `music_off` | `False` | Mute music. |
| `master_volume` | `1.0` | Global volume multiplier. |
| `music_volume` | `1.0` | Music-specific multiplier. |
| `sfx_volume` | `1.0` | SFX-specific multiplier. |
| `resolution` | `(800, 600)` | Window resolution (not fully wired yet). |
| `fullscreen` | `False` | Fullscreen flag. |

| Method | Description |
|---|---|
| `load()` | Load from `gamesettings/settings.json`. Prints a message if not found. |
| `save()` | Write current settings to JSON. |

---

### 5.8 DebugManager

**File**: `managers/debug_manager.py`  
**Singleton**: yes

Draws a semi-transparent overlay with FPS, CPU/RAM usage, camera position, and custom debug lines.

| Attribute | Default | Description |
|---|---|---|
| `debug_on` | `True` | Master debug toggle (F1 in main.py). |
| `debug_text` | `True` | Enable per-object text labels. |

| Method | Description |
|---|---|
| `update(dt)` | Update FPS counter and periodic system info. |
| `debug_draw()` | Draw the global debug overlay panel. |
| `begin_panel(x, y, …)` | Start a new text panel at position `(x, y)`. |
| `line(text, color)` | Print one line in the current panel (auto-wraps to columns). |
| `draw_debug_text(x, y, text, color)` | Draw a single string at an absolute position. |
| `draw_rect_overlay(x, y, w, h, color, alpha)` | Draw a translucent rectangle (useful for hitbox debugging). |

**Example** (inside a GameState's `debug_draw`):

```python
dm = self.debug_manager
dm.begin_panel(8, 300)
dm.line(f"player1 pos: {self.player1.world_pos}")
dm.line(f"on_ground: {self.player1.on_ground}")
```

---

### 5.9 EventManager

**File**: `managers/event_manager.py`

A lightweight observer/event-bus. **Not yet wired into the main system** – see `TODO.md`.

| Method | Description |
|---|---|
| `subscribe(event_name, callback)` | Register a listener function. |
| `unsubscribe(event_name, callback)` | Remove a listener. |
| `emit(event_name, data=None)` | Call all listeners for the event. |

**Example**:

```python
from managers.event_manager import EventManager

em = EventManager()

def on_hit(data):
    print(f"Hit! damage={data['damage']}")

em.subscribe("hit", on_hit)
em.emit("hit", {"damage": 25})
```

---

### 5.10 ParticleManager

**File**: `managers/particle_manager/particle_manager.py`

Simple particle system. Each `Particle` has a position, velocity, size, and shrinks over time.

| Method | Description |
|---|---|
| `emit(pos)` | Spawn one particle at `pos`. |
| `update(dt)` | Advance all particles and remove dead ones. |
| `draw(surface)` | Render all particles onto `surface`. |

---

## 6. Game Objects

### 6.1 Sprite

**File**: `gameobjects/sprite.py`

The lowest-level visual entity. Holds references to `AnimationData` from `GraphicManager` and handles frame advancement and rendering.

#### Key attributes

| Attribute | Description |
|---|---|
| `base_name` | Name of the currently loaded spritesheet. |
| `current_tag` | Active tag name (or `None` for whole-sheet playback). |
| `current_frame_idx` | Current frame index. |
| `active` | Whether animation advances each frame. |
| `visible` | Whether the sprite is drawn. |
| `flip_x` / `flip_y` | Horizontal / vertical flip. |
| `rotation` | Rotation in degrees (snapped to 45° for cache efficiency). |
| `scale` | Integer scale factor. |
| `png` | `True` when the loaded asset is a static PNG. |

#### Key methods

| Method | Returns | Description |
|---|---|---|
| `set_anim_name(name)` | `self` | Switch to a different spritesheet. Resets frame/tag. |
| `set_frame_tag(tag_name)` | `self` | Loop within a named tag. |
| `set_frame(index)` | `self` | Show one static frame (pauses animation). |
| `set_scale(scale)` | `self` | Switch to a different scale (creates scaled variant if needed). |
| `update(dt)` | — | Advance animation timer. |
| `draw(screen_pos, render_anchor)` | — | Blit the current frame to the game surface. |

All setters return `self` for **method chaining**:

```python
sprite = Sprite()
sprite.set_anim_name("hero").set_frame_tag("Walk").set_scale(2)
```

#### RenderAnchor enum

| Value | Meaning |
|---|---|
| `CENTER` | `screen_pos` is the centre of the sprite. |
| `TOPLEFT` | `screen_pos` is the top-left corner. |
| `BOTTOMCENTER` | `screen_pos` is the bottom-centre (good for characters standing on the ground). |

---

### 6.2 GameObject

**File**: `gameobjects/game_object.py`

Extends `Sprite` with a **world position**, optional **physics**, optional **camera projection**, and **hitbox/hurtbox** management.

#### Key attributes

| Attribute | Description |
|---|---|
| `world_pos` | `pygame.Vector2` – position in world space. |
| `vel` | `pygame.Vector2` – velocity (used by physics component). |
| `on_ground` | `bool` – set by the physics component each frame. |
| `physics` | Attached `PhysicsComponent` (or `None`). |
| `hitboxes` | `list[HitboxData]` |
| `hurtboxes` | `list[HurtboxData]` |

#### Key methods

| Method | Description |
|---|---|
| `add_physics(component)` | Attach a physics component (sets `component.owner = self`). |
| `enable_camera()` / `disable_camera()` | Toggle camera-relative rendering. |
| `add_hitbox(rect, type, base_name, tag_name, frame)` | Register a hitbox. `rect` is relative to `world_pos`. |
| `add_hurtbox(rect, type, base_name, tag_name, frame)` | Register a hurtbox. |
| `get_active_hitboxes()` | Returns `list[(world_rect, HitboxType)]` for currently active boxes. |
| `get_active_hurtboxes()` | Same for hurtboxes. |
| `update(dt)` | Ticks physics then `Sprite.update(dt)`. |
| `draw()` | Projects `world_pos` through the camera (if enabled) then calls `Sprite.draw()`. |

#### HitboxData / HurtboxData

Both have the same activation-filter API:

```python
HitboxData(
    rect=pygame.Rect(-10, -30, 20, 30),
    hitbox_type=HitboxType.HIGH,
    base_name="gbFighter",   # None = any spritesheet
    tag_name="Punch",        # None = any tag
    frame=2                  # None = all frames of tag
)
```

`is_active(current_base, current_tag, current_frame)` is evaluated automatically in `get_active_hitboxes()`.

---

### 6.3 BaseFighter

**File**: `gameobjects/base_fighter.py`

A `GameObject` with a `PlayerController` and `FighterPhysicsComponent` pre-attached. Intended as the base class for all playable characters.

| Attribute | Description |
|---|---|
| `speed` | Horizontal walk speed (passed to physics). |
| `facing_right` | `bool` – updated from input each frame. |
| `special_movelist` | `dict[str, list[Action]]` – motion inputs for specials. |
| `player_controller` | The attached `PlayerController`. |

`update(dt)` reads `player_controller.actions`, feeds directional input to `physics`, then calls `super().update(dt)`.

**Example**:

```python
from gameobjects.base_fighter import BaseFighter

player1 = BaseFighter(world_pos=(128, 228), player_index=0)
player1.set_anim_name("gbFighter").set_frame_tag("Idle").set_scale(3)
```

---

## 7. Components

### 7.1 PhysicsComponent / FighterPhysicsComponent

**File**: `gameobjects/components/physics_components.py`

A component that applies gravity, handles ground collision, and moves the owner's `world_pos`.

#### PhysicsComponent

| Parameter | Default | Description |
|---|---|---|
| `gravity` | 1180 | Pixels/s² downward acceleration. |
| `ground_y` | 400 | Y-coordinate of the ground plane. |
| `jump_speed` | 400 | Initial upward velocity on jump. |
| `walk_speed` | 100 | Horizontal speed (pixels/s). |

| Method | Description |
|---|---|
| `update(dt)` | Apply gravity, integrate velocity into `owner.world_pos`, detect ground. |
| `move_up()` | Apply jump if `on_ground`. |

#### FighterPhysicsComponent

Extends `PhysicsComponent` with fighter-specific defaults (`ground_y=420`, `jump_speed=600`) and left/right/stop methods.

| Method | Description |
|---|---|
| `move_left()` | Set `owner.vel.x = -walk_speed` (only on ground). |
| `move_right()` | Set `owner.vel.x = +walk_speed` (only on ground). |
| `stop()` | Set `owner.vel.x = 0` (only on ground). |
| `move_down()` | No-op placeholder. |

---

### 7.2 PlayerController

**File**: `gameobjects/components/player_controller_component.py`

Translates raw `InputManager` state into a per-frame `actions` dict and detects **special moves** via an input buffer.

| Attribute | Description |
|---|---|
| `actions` | `dict[Action, bool]` – current frame's pressed state. |
| `special_executed` | Name of any special move triggered this frame, or `None`. |
| `specialmovelist` | `dict[str, list[Action]]` – motions to detect (same format as `BaseFighter.special_movelist`). |

| Method | Description |
|---|---|
| `update(dt)` | Snapshot input, update buffer, check specials. |
| `is_action_pressed(action)` | `bool` – shorthand check. |
| `get_special_executed()` | Returns the special name if one fired this frame. |

**Buffer window**: 0.7 seconds. Diagonal combinations (e.g. DOWN + RIGHT) are automatically normalised to `Action.DOWN_RIGHT`.

---

## 8. Game States

### 8.1 GameState (abstract base)

**File**: `gamestates/gamestate.py`

All game states inherit from `GameState`. Every manager is immediately accessible via instance attributes.

```python
class GameState(ABC):
    self.gamestate_manager
    self.input_manager
    self.view_manager
    self.debug_manager
    self.sound_manager
    self.settings_manager
    self.camera          # shortcut for view_manager.camera

    # Built-in containers
    self.player1, self.player2  : GameObject | None
    self.stage                  : GameObject | None
    self.game_objects           : list[GameObject]
    self.projectiles_p1/p2      : list[GameObject]
```

#### Abstract methods you must implement

| Method | When called |
|---|---|
| `enter()` | When `GameStateManager.change_state()` switches to this state. |
| `exit()` | When leaving this state. |
| `handle_input()` | Before `update()`, every frame. |
| `update(dt)` | Every frame. **Call `super().update(dt)`** to tick all registered objects. |
| `draw()` | Every frame. **Call `super().draw()`** to draw stage → objects → players. |

#### Optional override

| Method | Description |
|---|---|
| `debug_draw()` | Called when `debug_on` is `True`. Default draws all objects' debug info. |
| `add_game_object(obj)` | Add an arbitrary `GameObject` to the state's update/draw list. |

---

### 8.2 TestState

**File**: `gamestates/teststate.py`

The currently active gameplay state. Demonstrates:

- Loading `Stage1` and configuring the camera.
- Creating two `BaseFighter` instances at specific world positions.
- Displaying an overlay sprite that is drawn on top of everything.
- Camera follow enabled with temporary keyboard overrides for manual camera movement.

---

## 9. Stages

### 9.1 BaseStage

**File**: `stages/base_stage.py`

Owns two `GameObject`s: `stage_front` (static HUD layer, no camera) and `stage_back` (scrolls with camera).

| Attribute | Description |
|---|---|
| `stage_front` | `GameObject` with `RenderAnchor.BOTTOMCENTER`. Not camera-affected. |
| `stage_back` | `GameObject` with `RenderAnchor.BOTTOMCENTER`. Typically camera-affected. |
| `stage_width` / `stage_height` | Set by the subclass after loading the sprite. |
| `allowed_camera_y_travel_min/max` | Vertical camera limits for this stage. |

| Method | Description |
|---|---|
| `configure_camera()` | Push stage dimensions, center, and travel limits into `Camera`. |
| `update(dt)` | Tick both layers. |
| `draw()` | Draw back then front. |
| `debug_draw()` | Debug-draw the back layer only. |

### 9.2 Stage1

**File**: `stages/stage1.py`

A concrete stage that loads `"stage1-front"` and `"stage1-back"` spritesheets at scale 3 and sets specific camera travel limits.

```python
from stages.stage1 import Stage1

self.stage = Stage1()       # world_pos defaults to (480, 470)
self.stage.configure_camera()
```

---

## 10. Utilities

### 10.1 globals.py

Color constants for use anywhere in the codebase:

```python
from globals import COLOR_RED, COLOR_GREEN, COLOR_YELLOW  # etc.
```

Available: `COLOR_RED`, `COLOR_GREEN`, `COLOR_BLUE`, `COLOR_WHITE`, `COLOR_BLACK`, `COLOR_YELLOW`, `COLOR_CYAN`, `COLOR_MAGENTA`, `COLOR_GRAY`, `COLOR_DARK_GRAY`, `COLOR_LIGHT_GRAY`.

### 10.2 decorators.py

```python
from decorators import singleton

@singleton
class MyManager:
    ...
```

Ensures only one instance is ever created. Subsequent calls to `MyManager()` return the existing instance.

---

## 11. How-To Guides

### 11.1 Add a new Game State

1. Create a file in `gamestates/`, e.g. `gamestates/menu_state.py`.
2. Subclass `GameState` and implement all abstract methods.

```python
from gamestates.gamestate import GameState

class MenuState(GameState):
    def enter(self):
        self.sound_manager.play_music("choices")

    def exit(self):
        self.sound_manager.stop_music()

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        from managers.input_manager import Action
        if Action.START in actions:
            self.gamestate_manager.change_state("gameplay")

    def update(self, dt):
        super().update(dt)

    def draw(self):
        super().draw()
```

3. Register it in `main.py`:

```python
from gamestates.menu_state import MenuState

sp.gamestate_manager.add_state("menu", MenuState())
sp.gamestate_manager.change_state("menu")
```

---

### 11.2 Create a new Fighter

1. Subclass `BaseFighter`.
2. Override `update()` to add character-specific logic.
3. Optionally override `special_movelist` with your character's moves.

```python
from gameobjects.base_fighter import BaseFighter
from managers.input_manager import Action

class Ryu(BaseFighter):
    def __init__(self, world_pos, player_index=0):
        super().__init__(world_pos, player_index)

        # Replace the default move list
        self.player_controller.specialmovelist = {
            "Hadouken": [Action.DOWN, Action.DOWN_RIGHT, Action.RIGHT, Action.A],
        }

    def update(self, dt):
        super().update(dt)
        # React to detected specials
        if self.player_controller.get_special_executed() == "Hadouken":
            print("Hadouken!")
```

Instantiate it in a `GameState.enter()`:

```python
self.player1 = Ryu(world_pos=(128, 228), player_index=0)
self.player1.set_anim_name("ryuSheet").set_frame_tag("Idle").set_scale(3)
```

---

### 11.3 Load and play a sprite animation

**Step 1 – Load in `main.py`** (once, before the main loop):

```python
sp.graphic_manager.load_spritesheet(
    "hero",
    "assets/Graphics/hero.png",
    "assets/Graphics/hero.json"
)
```

**Step 2 – Create a Sprite or GameObject and assign the animation**:

```python
from gameobjects.sprite import Sprite, RenderAnchor

icon = Sprite()
icon.set_anim_name("hero").set_frame_tag("Idle").set_scale(2)
```

**Step 3 – Tick and draw each frame**:

```python
# in update():
icon.update(dt)

# in draw():
icon.draw((400, 300), RenderAnchor.CENTER)
```

**Useful animation tricks**:

```python
sprite.flip_x = True          # mirror horizontally
sprite.rotation = 90           # rotate (snapped to 45° increments)
sprite.set_frame(0)            # freeze on frame 0
sprite.visible = False         # hide without removing
sprite.set_scale(4)            # change scale at runtime
```

---

### 11.4 Add a new Stage

1. Create `stages/my_stage.py` and subclass `BaseStage`.
2. Load your spritesheets and set the stage dimensions.

```python
from stages.base_stage import BaseStage

class MyStage(BaseStage):
    def __init__(self, world_pos=(480, 470)):
        super().__init__(world_pos=world_pos)

        self.stage_front.set_anim_name("myStage-front").set_frame_tag("Idle").set_scale(3)
        self.stage_back.set_anim_name("myStage-back").set_frame_tag("Idle").set_scale(3).enable_camera()

        self.stage_width = self.stage_front.sprite_size[0]
        self.stage_height = self.stage_front.sprite_size[1]

        self.allowed_camera_y_travel_min = -20
        self.allowed_camera_y_travel_max = 20

        self.configure_camera()
```

3. Don't forget to load both spritesheets in `main.py` before using the stage.
