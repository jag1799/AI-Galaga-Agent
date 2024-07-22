import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_settings, screen, ship):
       """Create a bullet object, at the ship's current position."""
       super(Bullet, self).__init__()
       self.screen = screen

       self.grid_size = ai_settings.grid_size
       

       # Create bullet rect at (0, 0), then set correct position.
       self.rect = pygame.Rect(
           0, 0, ai_settings.bullet_width, ai_settings.bullet_height
       )
       self.rect.centerx = ship.rect.centerx
       self.rect.top = ship.rect.top

       # Store a decimal value for the bullet's position.
       self.y = float(self.rect.y)

       self.color = ai_settings.bullet_color
       self.speed_factor = ai_settings.bullet_speed_factor

       # Track the last update time
       self.last_update_time = pygame.time.get_ticks()

    def update(self):
        """Move the bullet up the screen."""
        current_time = pygame.time.get_ticks()
        time_since_update = current_time - self.last_update_time
        
        if time_since_update >= 1000:
            # Update the decimal position of the bullet.
            self.y -= self.grid_size
            # Update the rect position.
            self.rect.y = round(self.y)
            self.last_update_time = current_time
        

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
