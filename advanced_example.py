"""
Advanced Platform Game Example
Demonstrates additional features that can be added to the basic platformer

This file shows examples of:
- Moving platforms
- Simple enemies
- Multiple levels
- Power-ups
- Particle effects
"""

import picosystem
import math
import random

# Enhanced game constants
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120
GRAVITY = 0.5
JUMP_STRENGTH = -8
PLAYER_SPEED = 2
MAX_LEVELS = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

class Particle:
    """Simple particle for visual effects"""
    
    def __init__(self, x, y, vel_x, vel_y, color, life):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.life = life
        self.max_life = life
    
    def update(self):
        """Update particle physics"""
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.1  # Light gravity
        self.life -= 1
        return self.life > 0
    
    def draw(self):
        """Draw the particle with fading alpha"""
        alpha = self.life / self.max_life
        if alpha > 0:
            picosystem.pen(*self.color)
            picosystem.pixel(int(self.x), int(self.y))

class MovingPlatform:
    """Platform that moves back and forth"""
    
    def __init__(self, x, y, width, height, move_range, speed, color=GRAY):
        self.start_x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_range = move_range
        self.speed = speed
        self.color = color
        self.direction = 1
        self.x = x
    
    def update(self):
        """Update platform movement"""
        self.x += self.speed * self.direction
        
        # Reverse direction at boundaries
        if self.x <= self.start_x:
            self.direction = 1
        elif self.x >= self.start_x + self.move_range:
            self.direction = -1
    
    def get_rect(self):
        """Get rectangle for collision detection"""
        return (self.x, self.y, self.width, self.height)
    
    def draw(self):
        """Draw the moving platform"""
        picosystem.pen(*self.color)
        picosystem.frect(int(self.x), self.y, self.width, self.height)
        
        # Draw direction indicator
        picosystem.pen(*WHITE)
        center_x = int(self.x + self.width // 2)
        center_y = self.y + self.height // 2
        if self.direction > 0:
            picosystem.pixel(center_x + 1, center_y)
        else:
            picosystem.pixel(center_x - 1, center_y)

class Enemy:
    """Simple enemy that moves back and forth"""
    
    def __init__(self, x, y, move_range, speed):
        self.start_x = x
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.move_range = move_range
        self.speed = speed
        self.direction = 1
    
    def update(self):
        """Update enemy movement"""
        self.x += self.speed * self.direction
        
        # Reverse direction at boundaries
        if self.x <= self.start_x:
            self.direction = 1
        elif self.x >= self.start_x + self.move_range:
            self.direction = -1
    
    def get_rect(self):
        """Get rectangle for collision detection"""
        return (self.x, self.y, self.width, self.height)
    
    def draw(self):
        """Draw the enemy"""
        picosystem.pen(*RED)
        picosystem.frect(int(self.x), int(self.y), self.width, self.height)
        
        # Draw angry eyes
        picosystem.pen(*WHITE)
        picosystem.pixel(int(self.x + 2), int(self.y + 2))
        picosystem.pixel(int(self.x + 5), int(self.y + 2))

class PowerUp:
    """Power-up that gives temporary abilities"""
    
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.power_type = power_type  # "speed", "jump", "invincible"
        self.collected = False
        self.bob_offset = 0
        self.flash_timer = 0
    
    def update(self):
        """Update power-up animation"""
        self.bob_offset = math.sin(picosystem.time() * 0.015) * 3
        self.flash_timer = (self.flash_timer + 1) % 20
    
    def get_rect(self):
        """Get rectangle for collision detection"""
        return (self.x, self.y + self.bob_offset, self.width, self.height)
    
    def draw(self):
        """Draw the power-up"""
        if not self.collected and self.flash_timer < 15:
            y_pos = int(self.y + self.bob_offset)
            
            if self.power_type == "speed":
                picosystem.pen(*GREEN)
            elif self.power_type == "jump":
                picosystem.pen(*PURPLE)
            elif self.power_type == "invincible":
                picosystem.pen(*ORANGE)
            
            picosystem.frect(self.x, y_pos, self.width, self.height)
            
            # Draw power indicator
            picosystem.pen(*WHITE)
            center_x = self.x + self.width // 2
            center_y = y_pos + self.height // 2
            
            if self.power_type == "speed":
                picosystem.pixel(center_x - 1, center_y)
                picosystem.pixel(center_x + 1, center_y)
            elif self.power_type == "jump":
                picosystem.pixel(center_x, center_y - 1)
                picosystem.pixel(center_x, center_y + 1)
            elif self.power_type == "invincible":
                picosystem.pixel(center_x, center_y)

class AdvancedPlayer:
    """Enhanced player with power-up support"""
    
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
        
        # Power-up states
        self.speed_boost = 0
        self.jump_boost = 0
        self.invincible = 0
        self.lives = 3
    
    def update(self, platforms, enemies, particles):
        """Update player with power-up effects"""
        # Update power-up timers
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.jump_boost > 0:
            self.jump_boost -= 1
        if self.invincible > 0:
            self.invincible -= 1
        
        # Handle input with power-up effects
        current_speed = PLAYER_SPEED * (2 if self.speed_boost > 0 else 1)
        
        if picosystem.pressed(picosystem.LEFT):
            self.vel_x = -current_speed
        elif picosystem.pressed(picosystem.RIGHT):
            self.vel_x = current_speed
        else:
            self.vel_x = 0
        
        # Jump with power-up effects
        if picosystem.pressed(picosystem.BUTTON_A) and self.on_ground:
            jump_power = JUMP_STRENGTH * (1.5 if self.jump_boost > 0 else 1)
            self.vel_y = jump_power
            self.on_ground = False
            
            # Jump particles
            for _ in range(3):
                particles.append(Particle(
                    self.x + random.randint(0, self.width),
                    self.y + self.height,
                    random.uniform(-1, 1),
                    random.uniform(-2, 0),
                    WHITE,
                    15
                ))
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Handle collisions
        self.handle_collisions(platforms)
        
        # Check enemy collisions
        if self.invincible == 0:
            self.check_enemy_collisions(enemies, particles)
        
        # Keep player on screen horizontally
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
    
    def handle_collisions(self, platforms):
        """Handle collision detection with platforms"""
        player_rect = (self.x, self.y, self.width, self.height)
        self.on_ground = False
        
        for platform in platforms:
            if self.rect_collision(player_rect, platform.get_rect()):
                # Handle moving platform
                if hasattr(platform, 'speed'):
                    self.x += platform.speed * platform.direction
                
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
    
    def check_enemy_collisions(self, enemies, particles):
        """Check collisions with enemies"""
        player_rect = (self.x, self.y, self.width, self.height)
        
        for enemy in enemies:
            if self.rect_collision(player_rect, enemy.get_rect()):
                self.take_damage(particles)
                break
    
    def take_damage(self, particles):
        """Handle taking damage"""
        self.lives -= 1
        self.invincible = 120  # 2 seconds of invincibility
        
        # Damage particles
        for _ in range(10):
            particles.append(Particle(
                self.x + self.width // 2,
                self.y + self.height // 2,
                random.uniform(-3, 3),
                random.uniform(-3, 1),
                RED,
                30
            ))
    
    def apply_powerup(self, power_type):
        """Apply a power-up effect"""
        if power_type == "speed":
            self.speed_boost = 300  # 5 seconds
        elif power_type == "jump":
            self.jump_boost = 300  # 5 seconds
        elif power_type == "invincible":
            self.invincible = 600  # 10 seconds
    
    def rect_collision(self, rect1, rect2):
        """Check if two rectangles collide"""
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and 
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def draw(self):
        """Draw the player with power-up effects"""
        # Flash when invincible
        if self.invincible > 0 and (self.invincible // 5) % 2:
            return
        
        # Color based on power-ups
        color = BLUE
        if self.speed_boost > 0:
            color = GREEN
        elif self.jump_boost > 0:
            color = PURPLE
        elif self.invincible > 0:
            color = ORANGE
        
        picosystem.pen(*color)
        picosystem.frect(int(self.x), int(self.y), self.width, self.height)
        
        # Draw eyes
        picosystem.pen(*WHITE)
        picosystem.pixel(int(self.x + 2), int(self.y + 2))
        picosystem.pixel(int(self.x + 5), int(self.y + 2))

# This is just an example file showing advanced features
# Copy the classes you want into your main.py file
print("This is an example file showing advanced features.")
print("Copy the classes you want into your main.py file.")