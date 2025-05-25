# Picosystem Platform Game

A simple 2D platformer game for the Picosystem handheld gaming device, written in MicroPython.

## Features

- **Player Character**: Blue character with physics-based movement
- **Gravity System**: Realistic falling and jumping mechanics
- **Platform Collision**: Multiple platforms to jump between
- **Collectibles**: Yellow items that bob up and down
- **Score System**: Collect items to increase your score
- **Level Completion**: Collect all items to complete the level

## Controls

- **Left/Right Arrow Keys**: Move the player left and right
- **A Button**: Jump (only when on ground)
- **X Button**: Restart the level

## Game Mechanics

### Player Physics
- Gravity constantly pulls the player downward
- Jump strength is fixed but feels responsive
- Horizontal movement has immediate response
- Player cannot move outside screen boundaries

### Collision Detection
- Rectangle-based collision system
- Player can land on top of platforms
- Player bounces off the bottom of platforms when jumping into them

### Collectibles
- Yellow squares that gently bob up and down
- Each collectible is worth 10 points
- Collect all items to complete the level

## Code Structure

### Classes

#### `Player`
Handles player movement, physics, and collision detection.
- Position and velocity tracking
- Input handling
- Collision detection with platforms
- Reset functionality

#### `Platform`
Represents static platforms in the game world.
- Rectangle collision bounds
- Drawing functionality
- Configurable size and color

#### `Collectible`
Animated items for the player to collect.
- Bobbing animation using sine wave
- Collision detection with player
- Collection state tracking

#### `Game`
Main game controller that manages all game objects.
- Level setup and layout
- Game state updates
- Rendering coordination
- Score tracking

## Installation and Setup

1. **Copy the Code**: Copy `main.py` to your Picosystem device
2. **Run the Game**: The game will start automatically when the device boots

## Customization Ideas

### Easy Modifications
- **Colors**: Change the color constants at the top of the file
- **Physics**: Adjust `GRAVITY`, `JUMP_STRENGTH`, and `PLAYER_SPEED`
- **Level Layout**: Modify the `setup_level()` method to create new platform arrangements

### Advanced Features to Add
- **Multiple Levels**: Create a level progression system
- **Enemies**: Add moving obstacles or enemies
- **Power-ups**: Special collectibles with temporary effects
- **Sound Effects**: Add audio feedback for jumps and collections
- **Animations**: Add sprite-based character animations
- **Moving Platforms**: Platforms that move back and forth

### Example Customizations

#### Change Player Color to Red
```python
# In the Player.draw() method, change:
picosystem.pen(*BLUE)
# to:
picosystem.pen(*RED)
```

#### Make Jumping Higher
```python
# Change the JUMP_STRENGTH constant:
JUMP_STRENGTH = -10  # Default is -8
```

#### Add More Collectibles
```python
# In the setup_level() method, add more lines like:
self.collectibles.append(Collectible(x, y))
```

## File Structure

```
├── main.py          # Main game file
└── README.md        # This documentation
```

## Performance Notes

- The game runs at 30 FPS on the Picosystem
- Collision detection is optimized for the small screen size
- All graphics are drawn using simple rectangles and pixels for optimal performance

## Troubleshooting

- **Game won't start**: Ensure the file is named exactly `main.py`
- **Controls not working**: Make sure you're using the correct button mappings for your Picosystem
- **Performance issues**: The game is optimized for the Picosystem's limited resources

## Credits

Created as a starting template for Picosystem game development. Feel free to modify and expand upon this code for your own games!
