import pyautogui

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
import game_functions as gf
import ai_agent as aag
from training import ActivityManager
import tqdm

class Game():

    def __init__(self, 
                 show_scoreboard = False, 
                 activity_manager : ActivityManager = None,
                 save_q_table = False,
                 load_q_table = False,
                 render_game = False,
                 index_log=[],
                 training=False
                 ):
        self.show_scoreboard = show_scoreboard
        self.activity_manager = activity_manager
        self.save_q_table = save_q_table
        self.load_q_table = load_q_table
        self.render_game = render_game
        self.index_log = index_log
        self.training = training
    
    """Initialize game variables and the main loop."""
    def run_game(self):
        # Initialize pygame, settings, and screen object.
        pygame.init()
        ai_settings = Settings(self.training)
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

        # Make a ship, a group of bullets, and a group of aliens.
        ship = Ship(ai_settings, screen)
        bullets = Group()
        aliens = Group()
        alien_bullets = Group()
        
        # Timing setup
        last_update_time = pygame.time.get_ticks()

        # Create the fleet of aliens.
        gf.create_fleet(ai_settings, screen, ship, aliens)
        
        if self.render_game:
            ai_settings.update_time_ms = 100
        else:
            ai_settings.update_time_ms = 10

        count = 0

        # Initialize the total number of states for the Q-table
        num_states = 20 # Could be -9 to +9, including None, 9 different alien ship heights, 9 different lowest bullets
       
        # Training mode has move left, move right. Non training hase left,right, fire bullet
        if self.training:
            num_actions = 2
        else:
            num_actions = 2
            
        if self.load_q_table:
            q_table = aag.load_q_table()
        else:
            q_table = aag.initialize_q_table(num_states, num_actions)
        
        # Initialize Q-learning parameters 
        alpha = 0.01 # learning rate
        gamma = 0.9 # discount factor 
        
        if self.training:
            epsilon = 0.90 # initial exploration rate
            epsilon_decay_rate = 0.999
        else:    
            epsilon = 0.0 # initial exploration rate
            epsilon_decay_rate = 0.99

        # Start the main loop for the game.
        while self.activity_manager.num_epochs <= self.activity_manager.max_epochs:

            # Reset the environment
            gf.check_events(
                ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, self.activity_manager,self.save_q_table,q_table,ai_settings.train_reward,ai_settings.event_count
            )
            if not stats.game_active:
                pyautogui.click()
            current_time = pygame.time.get_ticks()
            time_since_last_update = current_time - last_update_time
            
            # Track game stats
            if stats.game_active:

                ship.update()
                if aliens.sprites() != 0:
                    gf.fire_alien_bullets(ai_settings, screen, aliens, alien_bullets)
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, self.activity_manager)

                if time_since_last_update >= ai_settings.update_time_ms:  # 1000 milliseconds = 1 second

                    # Det the current state
                    state = aag.get_state(ship,aliens,alien_bullets)
                    current_index = aag.state_to_index(state)
        
                    # Determine next best action
                    action = aag.choose_action(state,q_table, epsilon)
                    
                    if self.training:
                        # perform the action in training mode with only move left and move right
                        aag.perform_action_training_mode(action, ai_settings, ship, screen, bullets, stats, sb, alien_bullets, aliens, self.activity_manager)
                        
                    else:
                        # perform the action
                        aag.perform_action(action, ai_settings, ship, screen, bullets, stats, sb, alien_bullets, aliens, self.activity_manager)
                                 
                    ai_settings.updated_this_iteration =False

                    for alien in aliens:
                        count = count+1
                        gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, self.activity_manager)
                    
                    if ai_settings.updated_this_iteration ==False:
                        aliens.update()
                  
                    ship.update()
                    if aliens.sprites() !=0:
                        gf.fire_alien_bullets(ai_settings, screen, aliens, alien_bullets)
                    gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, self.activity_manager)
                    
                    next_state = aag.get_state(ship, aliens, alien_bullets) 

                    # Get the rewards for the next state
                    reward = aag.get_rewards(next_state,ship, action)
                    train_reward_this_iteration= aag.get_train_rewards(next_state, ship, action)
                    
                    if self.training:
                        # Update Q-table
                        aag.update_q_table(current_index, action, train_reward_this_iteration, next_state, alpha, gamma, num_states, q_table)
                    else:
                        # Update Q-table ORiginal 
                        aag.update_q_table(current_index, action, reward, next_state, alpha, gamma, num_states, q_table)

                    # Reset the timer
                    last_update_time = current_time
                    
                    
                    # epsilon decay 
                    if epsilon > 0.00:
                        epsilon = epsilon * epsilon_decay_rate

                    
                    ai_settings.train_reward += train_reward_this_iteration
                    ai_settings.event_count += 1
                    self.index_log.append(current_index)

            gf.update_screen(
                ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, self.render_game
            )
  
        return self.index_log