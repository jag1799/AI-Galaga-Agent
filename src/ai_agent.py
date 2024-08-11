# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 10:15:51 2024

@author: PFINN
@author: JGERMANN
"""

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

import numpy as np


"""Determine the current state status."""
def get_state(ship : Ship, aliens, alien_bullets):

    ## Ship position
    ship_center = (ship.center-50)//100 # x-position 0 to 9
    
    # Alien bullet position
    alien_bullet_min_x = None

    if alien_bullets:
        # Find the bullet with the maximum y position
        # NOTE: Y position increases the further down the screen an object is.
        max_bullet = max(alien_bullets.sprites(), key=lambda bullet: bullet.rect.y)
        alien_bullet_min_x = max_bullet.rect.x // 100
    
    rel_ship_pos_x = None
    
    if alien_bullet_min_x != None :
        # Ship position relative to alien_bullets
        rel_ship_pos_x = alien_bullet_min_x - ship_center

    state = (rel_ship_pos_x)

    return state


"""Execute the action the agent chose for the current state."""
def perform_action(action, ai_settings, ship, screen, bullets, stats, sb, alien_bullets, aliens, activity_manager):
        
    ship.moving_left = False
    ship.moving_right = False

    if action == 0:  # Move left
        if ship.rect.left > ai_settings.grid_size:
            ship.moving_left = True
        if bullets !=0:  # Fire bullets
            gf.fire_bullet(ai_settings, screen, ship, bullets)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)   
    elif action == 1 :  # Move right
        if ship.rect.right < ai_settings.screen_width - ai_settings.grid_size:
            ship.moving_right = True
        if bullets !=0:  # Fire bullets
            gf.fire_bullet(ai_settings, screen, ship, bullets)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)

    gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)
    ship.update()

    return ship.rect.centerx

"""Execute the action chosen by the agent specifically in training mode."""
def perform_action_training_mode(action, ai_settings, ship, screen, bullets, stats, sb, alien_bullets, aliens, activity_manager):
        
    ship.moving_left = False
    ship.moving_right = False
            
    if action == 0:  # Move left
        if ship.rect.left > ai_settings.grid_size:
            ship.moving_left = True
    elif action == 1 :  # Move right
        if ship.rect.right < ai_settings.screen_width - ai_settings.grid_size:
            ship.moving_right = True

    gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, activity_manager)
    ship.update()

    return ship.rect.centerx


"""
Initialize the Q-Table at the start of a new Training run.

@note: Q-Table should NOT be reset at the start of an epoch.
"""
def initialize_q_table(num_states, num_actions):
    q_table = np.zeros((num_states, num_actions), dtype=np.float16)

    return q_table


"""Convert state to index."""
def state_to_index(state):
    
    if  state == None:
        state2 = 0
    elif state == -9:
        state2 = 1
    elif state == -8:
        state2 = 2
    elif state == -7:
        state2 = 3
    elif state == -6:
        state2 = 4
    elif state == -5:
        state2 = 5
    elif state == -4:
        state2 = 6
    elif state == -3:
        state2 = 7
    elif state == -2:
        state2 = 8
    elif state == -1:
        state2 = 9
    elif state == 0:
        state2 = 10
    elif state == 1:
        state2 = 11
    elif state == 2:
        state2 = 12
    elif state == 3:
        state2 = 13
    elif state == 4:
        state2 = 14
    elif state == 5:
        state2 = 15
    elif state == 6:
        state2 = 16
    elif state == 7:
        state2 = 17
    elif state == 8:
        state2 = 18
    elif state == 9:
        state2 = 19
     
    return state2


"""Select an action based on the current Q-Table."""
def choose_action(state,q_table,epsilon):
    
    state_index = state_to_index(state)
    
    # explore and choose a random action
    if np.random.rand() < epsilon:
        action_choice = np.random.choice(len(q_table[state_index]))
    else:
        action_choice = np.argmax(q_table[state_index])
    
    return action_choice


"""Get the rewards received during training."""
def get_train_rewards(next_state, ship, action):
    ship_center = (ship.center - 50) // 100  # x-position 0 to 9
    reward = 0

    if next_state is not None:
        bullet_position = next_state  # Relative position of the bullet

        # Reward for moving away from the bullet
        if bullet_position > 0:  # Bullet is to the left
            if action == 1:  # Moving right
                reward = 50
            else:  # Moving left
                reward = -50

        elif bullet_position < 0:  # Bullet is to the right
            if action == 0:  # Moving left
                reward = 50
            else:  # Moving right
                reward = -50

        else:  # Bullet is in the same column as the ship
            reward = -100  # Strong penalty for staying in the same column

    else:
        reward = 0  # No bullet present

    # Boundary penalty
    if (action == 1 and ship_center == 9) or (action == 0 and ship_center == 0):
        reward -= 100  # Penalty for trying to move beyond the boundary

    return reward


"""Get generic rewards received while not training."""
def get_rewards(next_state,ship, action):
    
    ship_center = (ship.center - 50) // 100  # x-position 0 to 9
    reward = 0

    if next_state is not None:
        bullet_position = next_state  # Relative position of the bullet

        # Reward for moving away from the bullet
        if bullet_position > 0:  # Bullet is to the left
            if action == 1:  # Moving right
                reward = 50
            else:  # Moving left
                reward = -50
        elif bullet_position < 0:  # Bullet is to the right
            if action == 0:  # Moving left
                reward = 50
            else:  # Moving right
                reward = -50
        else:  # Bullet is in the same column as the ship
            reward = -100  # Strong penalty for staying in the same column
    else:
        reward = 0  # No bullet present  
    
    # Boundary penalty
    if (action == 1 and ship_center == 9) or (action == 0 and ship_center == 0):
        reward -= 100  # Penalty for trying to move beyond the boundary

    return reward


"""Update all relevant states within the Q-Table."""
def update_q_table(current_index, action, reward, next_state, alpha, gamma, num_states, q_table):
    
    # Finding the row in the Q-table for the current state
    current_q_value = q_table[current_index][action]
        
    ## Finding the argmax Q value for next state
    next_state_index = state_to_index(next_state)    
    
    # Find the maximum Q-value for the next state
    next_state_q_value = np.max(q_table[next_state_index])

    # Calculate and update the Q-Value from the current state
    updated_q_value = current_q_value + alpha * (reward + gamma * next_state_q_value - current_q_value)

    q_table[current_index][action] = updated_q_value
    
    return q_table


"""Save the current Q-Table configuration as a CSV file."""
def save_q_table_as_csv(q_table):
    np.savetxt("q_table.csv",q_table,delimiter=",")


"""Load the specified CSV file into a numpy array representing the Q-Table."""
def load_q_table(filename="q_tableAgent Learned.csv"):
    return np.loadtxt(filename, delimiter=",")

























































