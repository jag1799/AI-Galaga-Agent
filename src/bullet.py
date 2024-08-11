import pygame
from pygame.sprite import Sprite

"""A class to manage bullets fired from the ship."""
class Bullet(Sprite):


    """Create a bullet object, at the ship's current position."""
    def __init__(self, ai_settings, screen, ship):
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
       
       # time interval to keep bullets on same interval with other updates
       self.update_int = ai_settings.update_time_ms


    """Move the bullet up the screen."""
    def update(self):
        current_time = pygame.time.get_ticks()
        time_since_update = current_time - self.last_update_time
        
        if time_since_update >= self.update_int:
            # Update the decimal position of the bullet.
            self.y -= self.grid_size
            # Update the rect position.
            self.rect.y = round(self.y)
            self.last_update_time = current_time


    """Draw the bullet to the screen."""
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
