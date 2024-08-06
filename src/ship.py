import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    """Initialize the ship, and set its starting position."""
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image, and get its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)        #############

        # Movement flags.
        self.moving_right = False
        self.moving_left = False

   
        # Keep track of time to control movement updates
        self.move_counter = 0
        self.move_delay = 10  # Adjust this to control movement frequency

    """Center the ship on the screen."""
    def center_ship(self):
        self.center = self.screen_rect.centerx+self.ai_settings.grid_size/2 


    """Update the ship's position, based on movement flags."""
    def update(self):
        self.move_counter+=1
        if self.move_counter >= self.move_delay:
            # Update the ship's center value, not the rect.
            if self.moving_right and self.rect.right <= self.screen_rect.right-self.ai_settings.grid_size/2:     ################
                self.center += self.ai_settings.grid_size 
                # Prevents continuous movement, requires key release
                self.moving_right = False
            if self.moving_left and self.rect.left >= 0+self.ai_settings.grid_size/2:        ##################
                self.center -= self.ai_settings.grid_size
                # Prevents continuous movement, requires key release
                self.moving_left=False
                
        # Update rect object from self.center.
        self.rect.centerx = self.center


    """Draw the ship at its current location."""
    def blitme(self):
        self.screen.blit(self.image, self.rect)
