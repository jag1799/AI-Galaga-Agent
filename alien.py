import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
    
        # Load the alien image.
        self.image = pygame.image.load("images/alien.bmp")
        
        # Assuming you have the width and height of the spaceship
        self.ship_width = 100
        self.ship_height = 100
    
        # Resize the alien image to match the spaceship size.
        self.image = pygame.transform.scale(self.image, (self.ship_width, self.ship_height))
        
        self.rect = self.image.get_rect()
    
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
    
        # Store the alien's exact position.
        self.x = float(self.rect.x)
        
        self.direction_change_count = 0  # Counts how many times the direction has changed

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    # def update(self):
    #     """Move the alien right or left."""
    #     self.x += 3 * self.ai_settings.fleet_direction
    #     self.rect.x = self.x  

    def update(self):
        """Move the alien right or left."""
        
        self.x += self.ai_settings.grid_size * self.ai_settings.fleet_direction
        self.rect.x = self.x  
        self.ai_settings.updated_this_iteration =True
        # self.x += self.ai_settings.grid_size/(self.ai_settings.num_alien_x * self.ai_settings.num_alien_y) * self.ai_settings.fleet_direction
        # self.rect.x = self.x  
       
        # self.x += self.ai_settings.grid_size/(self.ai_settings.num_alien_x * self.ai_settings.num_alien_y) * self.ai_settings.fleet_direction
             
        
        # self.ai_settings.count=self.ai_settings.count+1
        # print(f'self.x = {self.x}')
        # print(f'self.rect.x = {self.rect.x}')
        
        # print(f'self.ai_settings.fleet_direction = {self.ai_settings.fleet_direction}')
        
        # print(f'self.ai_settings.grid_size = {self.ai_settings.grid_size}')
        # print(f'self.ai_settings.count={self.ai_settings.count}')

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
