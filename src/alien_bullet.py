"""
Created Tues Jul 23 8:45:00

@author JGERMANN
"""

import pygame
from pygame.sprite import Group, Sprite
import random


"""
Bullet that an alien fires at random.  Maximum 3 bullets at a time.
"""
class Alien_Bullet(Sprite):
    
    bullet_active = False
    
    """Create a bullet at a random alien and fire it down the screen."""
    def __init__(self, ai_settings, screen, aliens : Group) -> None:
        super(Alien_Bullet, self).__init__()
        self.screen = screen

        self.grid_size = ai_settings.grid_size

        # Create a bullet at (0, 0), then set the correct position to a random alien.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        aliens_list = aliens.sprites()
        
        if not aliens_list:
            print("Warning: aliens_list is empty. Skipping bullet creation.")
           
            self.last_update_time =0

            # Store a decimal value for the bullet's position
            self.y = float(self.rect.y)

            # Settings for the bullet
            self.color = ai_settings.alien_bullet_color
            self.speed_factor = ai_settings.bullet_speed_factor
            
            # time interval to keep bullets on same interval with other updates
            self.update_int = ai_settings.update_time_ms
            return 
        self.last_update_time =0
        # time interval to keep bullets on same interval with other updates
        self.update_int = ai_settings.update_time_ms
        # Store a decimal value for the bullet's position
        self.y = float(self.rect.y)
        # Settings for the bullet
        self.color = ai_settings.alien_bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
        
        
        # Check if a bullet is already active
        if Alien_Bullet.bullet_active:
           return
       
        
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
    
        # Set the bullet_active flag to True
        Alien_Bullet.bullet_active = True
    
    """Move the Alien's bullet down the screen towards the ship"""
    def update(self):
        current_time = pygame.time.get_ticks()
        time_since_update = current_time - self.last_update_time

        if time_since_update >= self.update_int:
            # Update the decimal position of the alien's bullet.
            self.y += self.grid_size
            
            # Update the rect position.
            self.rect.y = round(self.y)
            self.last_update_time = current_time
            
            # Check if the bullet is off the screen and reset the flag
            if self.rect.top >= self.screen.get_rect().bottom:
                Alien_Bullet.bullet_active = False
                self.kill()  # Remove the bullet from the group

    """Draw the Alien bullet to the screen."""
    def draw_alien_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)