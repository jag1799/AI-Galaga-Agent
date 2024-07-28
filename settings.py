import sys
import pygame

class Settings:

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1000
        self.screen_height = 1000
        self.grid_size=100
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 200, 60, 60
        # Alien bullet color.
        self.alien_bullet_color = 160, 220, 150
        self.bullets_allowed = 3
        
        self.direction_change_interval = 1000  # Interval in milliseconds
        self.steps_to_move_right = 5
        self.steps_to_move_left = 10
        self.current_direction = 1  # 1 for right, -1 for left
        self.steps_moved = 0
        self.last_update_time = pygame.time.get_ticks()
        self.direction_change_steps = 5  # Number of steps before changing direction

        # Alien settings.
        self.fleet_drop_speed = 100

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5
        
        # Sets speed of frame updates/ gameplay speed
        self.update_time_ms = 5000
        
        # Flag for if the update occured during the current iteration
        self.updated_this_iteration =False
        
        # Testing Code 
        self.count = 0
        self.num_alien_x = 0 # only used as a counter for updates
        self.num_alien_y = 0 # only used as a counter for updates
        
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 25
        self.bullet_speed_factor = .1

        # Scoring.
        self.alien_points = 50

        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
