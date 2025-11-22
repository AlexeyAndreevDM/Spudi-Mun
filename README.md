# 🕷️ Spudi-Mun - 2D Spider-Man Game

<div align="center">

![Spider-Man](https://img.shields.io/badge/Spider--Man-2D%20Game-red)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![Status](https://img.shields.io/badge/Status-MVP%20Complete-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0--MVP-orange)

**A complete 2D Spider-Man experience with web-swinging, combat, and progression systems!**

</div>

## 🎮 Project Status - MVP Complete ✅

**Spudi-Mun has successfully reached its Minimum Viable Product (MVP) milestone!** The core gameplay experience is fully functional and polished:

### ✅ What's Complete:
- **🎯 Core Gameplay**: Fluid web-swinging physics and movement
- **⚔️ Combat System**: Melee combat with enemy AI and progression
- **👕 Suit System**: 8 unlockable Spider-Man suits
- **💾 Save/Load**: Complete save system with 6 slots
- **🎨 Visual Polish**: Scaling UI, damage effects, animations
- **🎵 Audio**: Full sound design and music integration
- **📱 Multi-Resolution**: Adaptive scaling for all screen sizes

### 🔄 Project State:
- **Current**: Stable MVP release
- **Active Development**: Paused
- **Maintenance**: Bug fixes only
- **Future Plans**: On hold until next development cycle

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Pygame 2.0+**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/spudi-mun.git
   cd spudi-mun
   ```

2. **Install dependencies**
   ```bash
   pip install pygame
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

## 🎯 Controls

| Action | Control | Description |
|--------|---------|-------------|
| **Movement** | `A/D` or `←/→` | Move left/right |
| **Jump** | `SPACE` | Vertical jump |
| **Web Swing** | `L-SHIFT` | Throw/web swing (hold) |
| **Attack** | `LMB` | Melee attack |
| **Heal** | `1` | Use concentration for healing |
| **Pause Menu** | `TAB` | Access suit selection & settings |
| **Exit** | `ESC` | Quit game |

## 🎮 Gameplay Systems

### 🕸️ Web-Swinging Mechanics

Experience true Spider-Man mobility with our advanced physics-based swinging system:

- **Momentum Conservation** - Swing speed decreases gradually over cycles
- **Directional Control** - Switch between right (`st=1`) and left (`st=-1`) swinging
- **Release Mechanics** - Perfect timing for maximum forward velocity
- **Aerial Recovery** - Return to swinging from free-fall with L-Shift

### ⚔️ Combat & Progression

```python
# Combat features integrated damage and progression systems
def attack(self, enemies, sdvigx):
    closest_enemy = self.find_closest_enemy(enemies)
    if closest_enemy and self.can_attack():
        closest_enemy.take_damage(self.attack_damage)
        self.increase_concentration()  # +5% per hit
        if closest_enemy.health <= 0:
            self.exp += 100  # Experience gain
```

**Combat Features:**
- **Smart Targeting** - Auto-targets nearest enemy in attack range
- **Concentration System** - Build focus with successful attacks
- **Healing Economy** - Convert concentration to health (2:1 ratio)
- **Experience Rewards** - 100 XP per enemy defeated

### 🎯 Enemy AI

Advanced enemy behavior with multiple states:

```python
class Enemy:
    def handle_behavior(self, player, player_world_x):
        distance = abs(player_world_x - self.world_x)
        
        if distance <= self.attack_range and self.attack_cooldown == 0:
            self.attack(player)  # Engage in combat
        elif distance <= self.detection_range:
            self.move_towards_player(player_world_x)  # Chase player
        else:
            self.patrol()  # Random patrol behavior
```

**AI States:**
- **🛡️ Patrol** - Random movement with occasional direction changes
- **🎯 Chase** - Accelerated pursuit when player detected
- **⚔️ Attack** - Engage when within attack range
- **🚫 Avoidance** - Prevent overlapping with other enemies

## 🎨 Visual & Audio Systems

### 🖼️ Scalable Graphics

```python
# Automatic scaling for all resolutions
SCALE = get_screen_scale()  # Auto-detects optimal scale
SCREEN_WIDTH = scale_value(BASE_SCREEN_WIDTH)
SCREEN_HEIGHT = scale_value(BASE_SCREEN_HEIGHT)

def scale_value(value):
    return int(value * SCALE)  # Universal scaling function
```

**Visual Features:**
- **Dynamic Damage Effects** - Red flash on hit, green on heal
- **Death Sequences** - Enhanced red border pulse effect
- **Camera Shake** - Screen shake on taking damage
- **Smooth Animations** - Fluid transitions between player states

### 🎵 Audio Experience

| Sound Type | Files | Usage |
|------------|-------|-------|
| **Web Sounds** | 4 variations | Swinging and web shooting |
| **Combat** | Punch, ground impact | Attacks and landings |
| **Healing** | 3 variations | Concentration usage |
| **Music** | Menu, gameplay themes | Atmospheric background |
| **Death** | Spider death sound | Player defeat |

## 🛠️ Technical Architecture

### 📁 Project Structure

```
Spudi-Mun/
├── 📄 main.py                 # Main game loop & state management
├── 📁 src/
│   ├── 📄 config.py           # Configuration, constants, paths
│   └── 📁 game/
│       ├── 📄 player.py       # Player class, movement, combat
│       └── 📄 enemy.py        # Enemy AI, behaviors, states
├── 📁 assets/
│   ├── 📁 images/            # Sprites, backgrounds, UI elements
│   ├── 📁 audio/             # Music and sound effects
│   └── 📁 fonts/             # Custom typography
└── 📁 data/
    └── 📁 saves/             # Game save data
```

### 🔧 Core Systems

**1. State Management**
```python
# Player movement states
PLAYER_STATES = {
    -100: "Initial Fall",
    0: "Grounded",
    1: "Right Swing", 
    -1: "Left Swing",
    2: "Post-Swing Flight",
    3: "Free Fall",
    4: "Jumping"
}
```

**2. Save System**
- **6 Save Slots** with automatic selection
- **Experience Persistence** across sessions
- **Slot Management** through main menu

**3. Difficulty Scaling**
```python
DIFFICULTY_SETTINGS = {
    'FN': 0.5,  # Friendly Neighborhood
    'TA': 1.0,  # The Amazing (Default)
    'S': 1.8,   # Spectacular
    'U': 3.0    # Ultimate
}
```

## 🎯 Game Modes & Progression

### 🏆 Difficulty Levels

| Level | Multiplier | Description |
|-------|------------|-------------|
| **Friendly Neighborhood** | 0.5x | Story-focused, relaxed combat |
| **The Amazing** | 1.0x | Balanced challenge (Default) |
| **Spectacular** | 1.8x | Enhanced enemy aggression |
| **Ultimate** | 3.0x | Maximum challenge for experts |

### 👕 Suit Collection

| Suit Code | Name | Status |
|-----------|------|--------|
| `cs` | Classic Suit | ✅ Available |
| `iss` | Iron Spider | ✅ Available |
| `ws` | Webbed Suit | ✅ Available |
| `us` | Upgraded Suit | ✅ Available |
| `ss` | Night Monkey | ✅ Available |
| `as` | Amazing Suit | ✅ Available |
| `is` | Integrated Suit | ✅ Available |
| `ads` | Advanced Suit | ✅ Available |

## 🐛 Known Issues & Solutions

| Issue | Status | Workaround |
|-------|--------|------------|
| Health text positioning | 🔄 Investigating | Manual position adjustment in code |
| Sound loading errors | ✅ Resolved | Fallback to placeholder system |
| Scaling on very small screens | ⚠️ Limited | Minimum scale of 0.8x enforced |

## 🔮 Roadmap

### 🎯 Short Term (Next Release)
- [ ] Additional enemy types and behaviors
- [ ] Expanded suit abilities and stats
- [ ] Boss battle implementations
- [ ] Enhanced visual effects

### 🚀 Medium Term
- [ ] Multi-level progression system
- [ ] Advanced skill trees
- [ ] Additional web-swinging mechanics
- [ ] Environmental interactions

### 🌟 Long Term
- [ ] Story mode with cutscenes
- [ ] Multiplayer cooperative modes
- [ ] Modding support and tools
- [ ] Mobile platform adaptation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Set up development environment
git clone [repository-url]
cd spudi-mun
pip install -r requirements.txt

# Run with debug mode
python main.py --debug
```

## 📊 Performance Notes

- **Target FPS**: 60 FPS stable
- **Memory Usage**: Optimized sprite loading
- **CPU Usage**: Efficient collision detection
- **Scaling**: Automatic adaptation to system capabilities

## 🎉 Acknowledgments

- **Spider-Man Character** - Marvel Comics
- **Pygame Community** - Game development framework
- **Sound Design** - Custom and sourced audio assets
- **Testing Team** - Quality assurance and feedback

---

<div align="center">

## 🕸️ Become Spider-Man!

**Experience the thrill of web-swinging through the city in this authentic 2D Spider-Man adventure!**

*"With great power comes great responsibility." - Uncle Ben*

</div>

---

*Spudi-Mun is a fan-made educational project. Spider-Man and related characters are trademarks of Marvel Comics. This project is not affiliated with or endorsed by Marvel.*
