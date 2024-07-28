"""
Created Tues Jul 23 8:45:00

@author JGERMANN
"""

import pygame
from pygame.sprite import Group, Sprite
import random

class Alien_Bullet(Sprite):
    """Bullet that an alien fires at random.  Maximum 3 bullets at a time."""
    
    def __init__(self, ai_settings, screen, aliens : Group) -> None:
        """Create a bullet at a random alien and fire it down the screen."""
        super(Alien_Bullet, self).__init__()
        self.screen = screen

        self.grid_size = ai_settings.grid_size

        # Create a bullet at (0, 0), then set the correct position to a random alien.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        aliens_list = aliens.sprites()
        # Get a random number within the remaining aliens
        alien_idx = random.randint(0, (len(aliens_list)-1))
        
        # Set initial hitboxes for the bullet
        self.rect.centerx = aliens_list[alien_idx].rect.centerx

        # This is different from the ship's bullet class since we're shooting downwards.
        self.rect.bottom = aliens_list[alien_idx].rect.bottom

        # Store a decimal value for the bullet's position
        self.y = float(self.rect.y)

        # Settings for the bullet
        self.color = ai_settings.alien_bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        # Track the last update time
        self.last_update_time = pygame.time.get_ticks()
        
        # time interval to keep bullets on same interval with other updates
        self.update_int = ai_settings.update_time_ms
        
    def update(self):
        """Move the Alien's bullet down the screen towards the ship"""
        current_time = pygame.time.get_ticks()
        time_since_update = current_time - self.last_update_time

        if time_since_update >= self.update_int:
            # Update the decimal position of the alien's bullet.
            self.y += self.grid_size
            
            # Update the rect position.
            self.rect.y = round(self.y)
            self.last_update_time = current_time

    def draw_alien_bullet(self):
        """Draw the Alien bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)