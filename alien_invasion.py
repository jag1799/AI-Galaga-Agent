import pyautogui

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
import ai_agent as aag
from training import ActivityManager


class Game():

    def __init__(self, 
                 show_scoreboard = False, 
                 debug = False,
                 activity_manager : ActivityManager = None):
        self.show_scoreboard = show_scoreboard
        self.debug = debug
        self.activity_manager = activity_manager
    
    """Initialize game variables and the main loop."""
    def run_game(self):
        # Initialize pygame, settings, and screen object.
        pygame.init()
        ai_settings = Settings()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(
            (ai_settings.screen_width, ai_settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics, and a scoreboard.
        stats = GameStats(ai_settings)

        if self.show_scoreboard:
            sb = Scoreboard(ai_settings, screen, stats)
        else:
            sb = None

        # Set the background color.
        bg_color = (230, 230, 230)

        # Make a ship, a group of bullets, and a group of aliens.
        ship = Ship(ai_settings, screen)
        bullets = Group()
        aliens = Group()
        alien_bullets = Group()
        
        # Timing setup
        last_update_time = pygame.time.get_ticks()

        # Create the fleet of aliens.
        gf.create_fleet(ai_settings, screen, ship, aliens)

        count = 0

        # Initialize the total number of states for the Q-table
        num_states = 10*1024*9*9*10 # the 1024 is really 385, but it was simpler to use 1024
        num_actions = 4
        q_table = aag.initialize_q_table(num_states, num_actions)
        
        # Initialize Q-learning parameters 
        alpha = 0.1
        gamma = 0.99
        # epsilon = 0.1 # exploration rate if greedy function is used.
        
        # Number of training instances completed
        num_epochs = 0 

        # Reward initialization 
        initial_lives = ai_settings.ship_limit
        initial_aliens = 8

        # Start the main loop for the game.
        while True:
            
            # Reset the environment
            gf.check_events(
                ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, self.activity_manager
            )
            if not stats.game_active:
                pyautogui.click()
            current_time = pygame.time.get_ticks()
            time_since_last_update = current_time - last_update_time
            
            # Track game stats
            if stats.game_active:

                ship.update()
                gf.fire_alien_bullets(ai_settings, screen, aliens, alien_bullets)
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, self.activity_manager)

                if time_since_last_update >= ai_settings.update_time_ms:  # 1000 milliseconds = 1 second
                    
                    ## Implementing AI Agent 
                    bullet_detected : float = 0

                    # Det the current state
                    state = aag.get_state(ship,aliens,alien_bullets)

                    # Check if a bullet was detected in any of the the detection squares
                    bullet_detected = state[len(state)-1]
                
                    # Determine next best action
                    action = aag.choose_action(state,q_table,num_states)
                
                    # perform the action
                    aag.perform_action(action, ai_settings, ship, screen, bullets, stats, sb,alien_bullets,aliens, self.activity_manager)

                    ai_settings.updated_this_iteration =False
                    for alien in aliens:
                        count = count+1
                        alienx = alien.x
                        gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, self.activity_manager)
                    
                    if ai_settings.updated_this_iteration ==False:
                        aliens.update()
                        
                        # print(f'count = {count} aliens.x = {alienx}')
                                            
                    next_state = aag.get_state(ship, aliens, alien_bullets)  
                    
                    # Get the rewards for the next state
                    reward = aag.get_rewards(len(bullets),initial_lives,stats.ships_left,initial_aliens,len(aliens), bullet_detected)
                    
                    # Update Q-table
                    aag.update_q_table(state, action, reward, next_state, alpha, gamma, num_states, q_table)

                    # Reset the timer
                    last_update_time = current_time  
        
            gf.update_screen(
                ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets
            )