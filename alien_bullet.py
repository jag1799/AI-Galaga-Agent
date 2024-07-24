import pygame
from pygame.sprite import _Group, Sprite
import random

class Alien_Bullet(Sprite):

    def __init__(self, ai_settings, screen, aliens) -> None:
        super(Alien_Bullet, self).__init__()
        self.screen = screen

        self.grid_size = ai_settings.grid_size

        # Create a bullet at (0, 0), then set the correct position to a random alien.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        
        # Get a random number within the remaining aliens
        alien_idx = random.randint(0, len(aliens))

        print(alien_idx)
        
        # Get the position of a random alien
        

        # Store a decimal value for the bullet's position

        # Settings for the bullet

        # Track the last update time
        self.last_update_time = pygame.time.get_ticks()
    
    def update_alien_bullet(self):
        """Move the Alien's bullet down the screen towards the ship"""
        current_time = pygame.time.get_ticks()
        time_since_update = current_time - self.last_update_time

        if time_since_update >= 1000:
            # Update the decimal position of the alien's bullet.
            self.y -= self.grid_size
            
            # Update the rect position.
            self.rect.y = round(self.y)
            self.last_update_time = current_time

    def draw_alien_bullet(self):
        """Draw the Alien bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)