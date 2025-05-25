"""
Picosystem Platform Game with Horizontal Scrolling
A 2D platformer game for the Picosystem with Mario-style camera scrolling

Controls:
- Left/Right: Move player
- A Button: Jump
- X Button: Restart level
"""

import picosystem
import math
import random

# Game constants
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120
GRAVITY = 0.5
JUMP_STRENGTH = -8
PLAYER_SPEED = 2

# Level constants
LEVEL_WIDTH = 480  # 4 screens wide
CAMERA_FOLLOW_SPEED = 0.1  # How smoothly camera follows player
CAMERA_OFFSET = 40  # Player position relative to left edge of screen

# Colors
BLACK = (0, 0, 0)        # 0
WHITE = (15, 15, 15)     # 15
RED = (15, 0, 0)         # 2
GREEN = (0, 15, 0)       # 3
BLUE = (0, 0, 15)        # 4
YELLOW = (15, 15, 0)     # 5
GRAY = (8, 8, 8)         # 7 (approximate mid-gray)
BROWN = (8, 4, 0)        # 9 (approximate brown)

class Camera:
    """Camera system for horizontal scrolling"""
    
    def __init__(self):
        self.x = 0
        self.target_x = 0
    
    def update(self, player_x):
        """Update camera to follow player"""
        # Calculate target camera position
        self.target_x = player_x - CAMERA_OFFSET
        
        # Clamp camera to level boundaries
        self.target_x = max(0, min(self.target_x, LEVEL_WIDTH - SCREEN_WIDTH))
        
        # Smooth camera movement
        self.x += (self.target_x - self.x) * CAMERA_FOLLOW_SPEED
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        return (world_x - self.x, world_y)
    
    def is_on_screen(self, world_x, width=0):
        """Check if an object is visible on screen"""
        return (world_x + width >= self.x and world_x <= self.x + SCREEN_WIDTH)

class Player:
    """Player character with physics and controls"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.start_x = x
        self.start_y = y
    
    def update(self, platforms):
        """Update player physics and handle input"""
        # Handle input
        if picosystem.button(picosystem.LEFT):
            self.vel_x = -PLAYER_SPEED
        elif picosystem.button(picosystem.RIGHT):
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x = 0
        
        # Jump
        if picosystem.pressed(picosystem.A) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y

        #print("Player position:", self.x, self.y, "Velocity:", self.vel_x, self.vel_y, end='\r')
        
        # Handle collisions
        self.handle_collisions(platforms)
        
        # Keep player within level boundaries
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > LEVEL_WIDTH:
            self.x = LEVEL_WIDTH - self.width
    
    def handle_collisions(self, platforms):
        """Handle collision detection with platforms"""
        player_rect = (self.x, self.y, self.width, self.height)
        self.on_ground = False
        
        for platform in platforms:
            if self.rect_collision(player_rect, platform.get_rect()):
                # Determine collision direction
                if self.vel_y > 0:  # Falling down
                    if self.y < platform.y:  # Landing on top
                        self.y = platform.y - self.height
                        self.vel_y = 0
                        self.on_ground = True
                elif self.vel_y < 0:  # Moving up
                    if self.y > platform.y:  # Hitting from below
                        self.y = platform.y + platform.height
                        self.vel_y = 0
    
    def rect_collision(self, rect1, rect2):
        """Check if two rectangles collide"""
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and 
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def reset(self):
        """Reset player to starting position"""
        self.x = self.start_x
        self.y = self.start_y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
    
    def draw(self, camera):
        """Draw the player"""
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        
        # Only draw if on screen
        if camera.is_on_screen(self.x, self.width):
            picosystem.pen(*BLUE)
            picosystem.frect(int(screen_x), int(screen_y), self.width, self.height)
            
            # Draw eyes
            picosystem.pen(*WHITE)
            picosystem.pixel(int(screen_x + 2), int(screen_y + 2))
            picosystem.pixel(int(screen_x + 5), int(screen_y + 2))


class Platform:
    """A platform that the player can stand on"""
    
    def __init__(self, x, y, width, height, color=BROWN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def get_rect(self):
        """Get rectangle representation for collision detection"""
        return (self.x, self.y, self.width, self.height)
    
    def draw(self, camera):
        """Draw the platform"""
        # Only draw if visible on screen
        if camera.is_on_screen(self.x, self.width):
            screen_x, screen_y = camera.world_to_screen(self.x, self.y)
            picosystem.pen(*self.color)
            picosystem.frect(int(screen_x), int(screen_y), self.width, self.height)
            
            # Add some detail to platforms
            picosystem.pen(*DARK_BROWN)
            picosystem.hline(int(screen_x), int(screen_y), self.width)
            if self.height > 4:
                picosystem.pen(*LIGHT_BROWN)
                picosystem.hline(int(screen_x), int(screen_y + 1), self.width)


class Collectible:
    """Collectible items for the player to gather"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 6
        self.collected = False
        self.bob_offset = 0
        self.tick_counter = 0
    
    def update(self):
        """Update collectible animation using ticks"""
        self.tick_counter += 1
        # Use sine wave with tick counter for smooth bobbing
        # Divide by larger number for slower animation, smaller for faster
        self.bob_offset = math.sin(self.tick_counter * 0.1) * 2
    
    def get_rect(self):
        """Get rectangle for collision detection"""
        return (self.x, self.y + self.bob_offset, self.width, self.height)
    
    def draw(self, camera):
        """Draw the collectible"""
        if not self.collected and camera.is_on_screen(self.x, self.width):
            screen_x, screen_y = camera.world_to_screen(self.x, self.y)
            y_pos = int(screen_y + self.bob_offset)
            
            picosystem.pen(*YELLOW)
            picosystem.frect(int(screen_x), y_pos, self.width, self.height)
            
            # Draw shine effect
            picosystem.pen(*WHITE)
            picosystem.pixel(int(screen_x + 1), y_pos + 1)


class Game:
    """Main game class with scrolling camera"""
    
    def __init__(self):
        self.player = Player(50, 80)
        self.camera = Camera()
        self.platforms = []
        self.collectibles = []
        self.score = 0
        self.setup_level()
    
    def setup_level(self):
        """Create a larger scrolling level layout"""
        self.platforms.clear()
        self.collectibles.clear()
        
        # Ground platforms - create a continuous ground
        for x in range(0, LEVEL_WIDTH, 60):
            self.platforms.append(Platform(x, 110, 60, 10))
        
        # Starting area platforms
        self.platforms.append(Platform(30, 90, 20, 8))
        self.platforms.append(Platform(70, 80, 25, 8))
        
        # Section 1 (Screen 1-2)
        self.platforms.append(Platform(120, 95, 30, 8))
        self.platforms.append(Platform(170, 85, 20, 8))
        self.platforms.append(Platform(210, 75, 25, 8))
        self.platforms.append(Platform(160, 65, 15, 8))
        self.platforms.append(Platform(250, 90, 30, 8))
        
        # Section 2 (Screen 2-3) - Higher platforms
        self.platforms.append(Platform(300, 100, 25, 8))
        self.platforms.append(Platform(340, 85, 20, 8))
        self.platforms.append(Platform(280, 70, 15, 8))
        self.platforms.append(Platform(320, 55, 20, 8))
        self.platforms.append(Platform(370, 70, 25, 8))
        self.platforms.append(Platform(410, 55, 20, 8))
        
        # Section 3 (Screen 3-4) - Challenge area
        self.platforms.append(Platform(450, 95, 15, 8))
        self.platforms.append(Platform(420, 80, 15, 8))
        self.platforms.append(Platform(390, 65, 15, 8))
        self.platforms.append(Platform(360, 50, 15, 8))
        self.platforms.append(Platform(330, 35, 15, 8))
        self.platforms.append(Platform(370, 25, 30, 8))  # Victory platform
        
        # Add floating platforms for variety
        self.platforms.append(Platform(100, 50, 15, 6))
        self.platforms.append(Platform(180, 45, 15, 6))
        self.platforms.append(Platform(260, 40, 15, 6))
        self.platforms.append(Platform(340, 35, 15, 6))
        
        # Collectibles spread across the level
        collectible_positions = [
            (35, 82), (125, 87), (175, 77), (215, 67), (265, 82),
            (305, 92), (285, 62), (325, 47), (375, 62), (415, 47),
            (395, 57), (365, 42), (335, 27), (385, 17), (80, 42),
            (185, 37), (265, 32), (345, 27), (455, 87), (425, 72)
        ]
        
        for x, y in collectible_positions:
            self.collectibles.append(Collectible(x, y))
    
    def update(self):
        """Update game state"""
        # Handle restart
        if picosystem.pressed(picosystem.X):
            self.restart_level()
            return
        
        # Update player
        self.player.update(self.platforms)
        
        # Update camera to follow player
        self.camera.update(self.player.x)
        
        # Update collectibles
        for collectible in self.collectibles:
            collectible.update()
            
            # Check collision with player
            if not collectible.collected:
                player_rect = (self.player.x, self.player.y, 
                             self.player.width, self.player.height)
                if self.player.rect_collision(player_rect, collectible.get_rect()):
                    collectible.collected = True
                    self.score += 10
        
        # Check if player fell off screen
        if self.player.y > SCREEN_HEIGHT + 20:
            self.restart_level()
    
    def restart_level(self):
        """Restart the current level"""
        self.player.reset()
        self.camera.x = 0
        self.camera.target_x = 0
        self.score = 0
        for collectible in self.collectibles:
            collectible.collected = False
    
    def draw(self):
        """Draw the game with camera scrolling"""
        # Clear screen
        picosystem.pen(*BLACK)
        picosystem.clear()
        
        # Draw background elements (optional - could add clouds, etc.)
        self.draw_background()
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.camera)
        
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.draw(self.camera)
        
        # Draw player
        self.player.draw(self.camera)
        
        # Draw UI (always on screen)
        self.draw_ui()
    
    def draw_background(self):
        """Draw scrolling background elements"""
        # Simple parallax background - draw some distant objects
        for i in range(0, LEVEL_WIDTH, 80):
            # Background "mountains" that scroll slower than camera
            bg_x = i - (self.camera.x * 0.3)  # Parallax effect
            if bg_x > -20 and bg_x < SCREEN_WIDTH + 20:
                picosystem.pen(*GRAY)
                # Simple triangle for distant hills
                for y in range(5):
                    picosystem.hline(int(bg_x + 10 - y), int(80 + y), y * 2)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Draw score
        picosystem.pen(*WHITE)
        picosystem.text(f"Score: {self.score}", 2, 2)
        
        # Draw progress indicator
        progress = min(100, int((self.player.x / LEVEL_WIDTH) * 100))
        picosystem.text(f"Progress: {progress}%", 2, 12)
        
        # Draw controls hint
        picosystem.text("X: Restart", 2, SCREEN_HEIGHT - 10)
        
        # Check for level completion
        all_collected = all(c.collected for c in self.collectibles)
        if all_collected:
            picosystem.pen(*GREEN)
            picosystem.text("Level Complete!", 25, 60)
            picosystem.text("Press X to restart", 15, 70)


# Global game instance
game = Game()

def update(tick):
    """Main update function called by picosystem"""
    game.update()
    # Uncomment if you want to see a countdown
    #if tick % 10 == 0:
    #    print("Count down to auto quit: ", 1000 - tick, end='\r')

    # Auto quit after 1000 ticks
    if tick > 1000:
        quit()

def draw(tick):
    """Main draw function called by picosystem"""
    game.draw()



picosystem.start()
