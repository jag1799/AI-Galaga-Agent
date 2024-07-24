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


    # def __init__(self, ai_settings, screen):
    #     """Initialize the alien, and set its starting position."""
    #     super(Alien, self).__init__()
    #     self.screen = screen
    #     self.ai_settings = ai_settings

    #     # Load the alien image, and set its rect attribute.
    #     self.image = pygame.image.load("images/alien.bmp")
    #     self.rect = self.image.get_rect()

    #     # Start each new alien near the top left of the screen.
    #     self.rect.x = self.rect.width
    #     self.rect.y = self.rect.height
        
            

    #     # Store the alien's exact position.
    #     self.x = float(self.rect.x)
        
    #     self.direction_change_count = 0  # Counts how many times the direction has changed
   

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    
    def update(self):
        """Move the alien right or left."""
        self.x += 3 * self.ai_settings.fleet_direction
        self.rect.x = self.x
        
        # # Pause the game and wait for Enter
        # input("Press Enter to continue...")
        # print(self.rect)

    # def update(self):
    #     """Move the alien right or left."""
        
    #     current_time = pygame.time.get_ticks()
    #     time_since_update = current_time - self.ai_settings.last_update_time
        
    #     move_distance = 100  # or any distance you want
        
        
        
        
        
    #     if time_since_update >= self.ai_settings.direction_change_interval:
    #         # Move the alien
    #         self.x += self.ai_settings.grid_size * self.ai_settings.current_direction
    #         print(self.ai_settings.grid_size * self.ai_settings.current_direction )
    #         self.rect.x = round(self.x)
    #         self.ai_settings.steps_moved += 1

    #     # Change direction if needed
    #     if self.ai_settings.steps_moved >= self.ai_settings.steps_to_move_right:
    #         self.ai_settings.current_direction = -1
    #         self.ai_settings.steps_moved = 0
    #         self.ai_settings.steps_to_move_right = self.ai_settings.steps_to_move_left
    #         self.ai_settings.steps_to_move_left = 0  # Or set another value if needed
            
    #     elif self.ai_settings.steps_moved >= self.ai_settings.steps_to_move_left:
    #         self.ai_settings.current_direction = 1
    #         self.ai_settings.steps_moved = 0
    #         self.ai_settings.steps_to_move_left = self.ai_settings.steps_to_move_right
    #         self.ai_settings.steps_to_move_right = 0  # Or set another value if needed

        # # Update the last update time
        # self.ai_settings.last_update_time = current_time  
        
        # self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        # self.rect.x = self.x
        
        

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
