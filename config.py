"""
Game Configuration
Easily modify game settings and constants

To use this config:
1. Import at the top of main.py: from config import *
2. Replace hardcoded values with these constants
"""

# Screen settings
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120

# Physics constants
GRAVITY = 0.5          # How fast objects fall (0.3 = slow, 0.8 = fast)
JUMP_STRENGTH = -8     # How high the player jumps (-6 = low, -12 = high)
PLAYER_SPEED = 2       # How fast the player moves (1 = slow, 4 = fast)

# Game settings
PLAYER_LIVES = 3       # Number of lives the player starts with
COLLECTIBLE_POINTS = 10  # Points earned per collectible

# Player settings
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8

# Colors (R, G, B) - values from 0 to 15 for picosystem
BLACK = (0, 0, 0)
WHITE = (15, 15, 15)
RED = (15, 0, 0)
GREEN = (0, 15, 0)
BLUE = (0, 0, 15)
YELLOW = (15, 15, 0)
GRAY = (8, 8, 8)
BROWN = (8, 4, 1)
PURPLE = (8, 0, 8)
ORANGE = (15, 10, 0)
PINK = (15, 12, 13)
CYAN = (0, 15, 15)

# Color themes - uncomment one to use
# PLAYER_COLOR = BLUE      # Default
# PLAYER_COLOR = RED       # Red player
# PLAYER_COLOR = GREEN     # Green player
# PLAYER_COLOR = PURPLE    # Purple player

# PLATFORM_COLOR = BROWN   # Default
# PLATFORM_COLOR = GRAY    # Gray platforms
# PLATFORM_COLOR = GREEN   # Green platforms

# COLLECTIBLE_COLOR = YELLOW  # Default
# COLLECTIBLE_COLOR = PINK    # Pink collectibles
# COLLECTIBLE_COLOR = CYAN    # Cyan collectibles

# Level layouts - each tuple is (x, y, width, height)
LEVEL_1_PLATFORMS = [
    # Ground platforms
    (0, 110, 40, 10),
    (60, 110, 60, 10),
    
    # Mid-level platforms
    (30, 90, 20, 8),
    (70, 80, 25, 8),
    (15, 70, 20, 8),
    (80, 60, 30, 8),
    
    # Upper platforms
    (10, 50, 25, 8),
    (50, 40, 30, 8),
    (90, 30, 25, 8),
    
    # Top platform
    (40, 20, 40, 8),
]

# Collectible positions for level 1 - each tuple is (x, y)
LEVEL_1_COLLECTIBLES = [
    (35, 82),
    (78, 72),
    (20, 62),
    (88, 52),
    (20, 42),
    (65, 32),
    (98, 22),
    (55, 12),
]

# Alternative level layout - more challenging
LEVEL_2_PLATFORMS = [
    # Ground
    (0, 110, 20, 10),
    (100, 110, 20, 10),
    
    # Scattered platforms
    (40, 100, 15, 8),
    (20, 85, 15, 8),
    (80, 85, 15, 8),
    (50, 70, 15, 8),
    (10, 55, 15, 8),
    (90, 55, 15, 8),
    (35, 40, 15, 8),
    (70, 40, 15, 8),
    (55, 25, 15, 8),
]

LEVEL_2_COLLECTIBLES = [
    (45, 92),
    (25, 77),
    (85, 77),
    (55, 62),
    (15, 47),
    (95, 47),
    (40, 32),
    (75, 32),
    (60, 17),
]

# Easy mode settings
EASY_MODE = {
    'GRAVITY': 0.3,
    'JUMP_STRENGTH': -10,
    'PLAYER_SPEED': 3,
    'PLAYER_LIVES': 5,
}

# Hard mode settings
HARD_MODE = {
    'GRAVITY': 0.7,
    'JUMP_STRENGTH': -6,
    'PLAYER_SPEED': 1.5,
    'PLAYER_LIVES': 1,
}

# Control mappings (for reference)
CONTROLS = {
    'MOVE_LEFT': 'picosystem.LEFT',
    'MOVE_RIGHT': 'picosystem.RIGHT', 
    'JUMP': 'picosystem.BUTTON_A',
    'RESTART': 'picosystem.BUTTON_X',
}

# Animation settings
COLLECTIBLE_BOB_SPEED = 0.01   # How fast collectibles bob up and down
COLLECTIBLE_BOB_HEIGHT = 2     # How far collectibles move up and down

# UI settings
SCORE_X = 2
SCORE_Y = 2
UI_TEXT_COLOR = WHITE

# Sound settings (if you add sound later)
SOUND_ENABLED = True
JUMP_SOUND_PITCH = 440    # Hz
COLLECT_SOUND_PITCH = 880  # Hz