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
import hashlib

"""Determine the current state status."""
def get_state(ship : Ship, aliens, alien_bullets):

    ## Ship position
    ship_center = (ship.center - 50) // 100 # x-position 0 to 9

    ## Alien positions 
    alien_x_columns = np.zeros(10, dtype = int)
    lowest_alien_y = 0
    for alien in aliens:
        # Gathering alien x,y info
        x_pixel, y_pixel = alien.x // 100, alien.rect.y // 100 
        # Placing alien x info into a 1 for presence in a column
        alien_x_columns[x_pixel] = 1
        
        lowest_alien_y = max(lowest_alien_y, y_pixel)
        
    ## Convert alien_x_columns to an integer
    binary_string = ''.join(map(str, alien_x_columns))
    alien_x_columns_int = int(binary_string, 2)
    
    # Alien bullet position
    alien_bullet_min_y = None
    alien_bullet_min_x = None
    if alien_bullets:
        # Find the bullet with the maximum y position
        # NOTE: Y position increases the further down the screen an object is.
        max_bullet = max(alien_bullets.sprites(), key=lambda bullet: bullet.rect.y)
        alien_bullet_min_y = (max_bullet.rect.y + 15) // 100 - 1
        alien_bullet_min_x = max_bullet.rect.x // 100

    relative_x_ship_position = 1000

    if alien_bullet_min_x != None:
        # Ship Position relative to alien bullets
        relative_x_ship_position = alien_bullet_min_x - ship_center
    
    if relative_x_ship_position > 2 or relative_x_ship_position < -2:
        relative_x_ship_position = None
    
    if alien_bullet_min_y != None and alien_bullet_min_y < 7:
        alien_bullet_min_y = None
    elif alien_bullet_min_y != None:
        alien_bullet_min_y = 9 - alien_bullet_min_y # 0 if at the same level as the ship, 1 if 1 ahead of the ship.

    state = (relative_x_ship_position, lowest_alien_y, alien_bullet_min_y)
    return state
    
"""Execute the agent selected action per the game rules."""
def perform_action(action, ai_settings, ship, screen, bullets, stats, sb, alien_bullets, aliens, activity_manager):
    if action == 0:  # Fire bullets
        gf.fire_bullet(ai_settings, screen, ship, bullets)
        # gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
    elif action == 1:  # Move left
        if ship.rect.left > ai_settings.grid_size:
            ship.moving_left = True
        else:
            ship.moving_left = False
    elif action == 2:  # Move right
        if ship.rect.right < ai_settings.screen_width - ai_settings.grid_size:
            ship.moving_right = True
        else:
            ship.moving_right = False
    elif action == 3:
        pass
    
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
def state_to_index(state, num_states):
    # convert state to string
    state_str = str(state)
    
    #create stable hash
    hash_object = hashlib.sha256(state_str.encode())
    
    hash_int = int(hash_object.hexdigest(),16)
    state_index = hash_int % num_states

    return state_index

"""Select an action based on the current Q-Table."""
def choose_action(state, q_table, num_states, epsilon):
    
    state_index = state_to_index(state,num_states)

    # If we're early in the exploration, choose random choices, otherwise, exploit the known states.
    if np.random.rand() < epsilon:
        action_choice = np.random.choice(len(q_table[state_index]))
    else:
        action_choice = np.argmax(q_table[state_index])
    
    return action_choice

"""Calculate the new overall reward."""
def get_rewards(num_bullets, initial_aliens, aliens_left, next_state):
    
    reward = 0
    
    # Reward pertaining to the number of bullets fired
    bullet_reward =-0.05*num_bullets
    
    if next_state[0] != None:
        alien_bullet_reward_x = -(3 - abs(next_state[0]))
    else:
        alien_bullet_reward_x = 0
    
    if next_state[2] != None:
        alien_bullet_reward_y = -(3 - next_state[2])
    else:
        alien_bullet_reward_y = 0

    # Reward pertaining to the number of aliens
    aliens_left_reward = (initial_aliens-aliens_left)*.1
    
    reward = bullet_reward + aliens_left_reward + alien_bullet_reward_x + alien_bullet_reward_y
    
    return reward

"""Update all relevant states within the Q-Table."""
def update_q_table(current_index, action, reward, next_state, alpha, gamma, num_states, q_table):
    
    # Finding the row in the Q-table for the current state
    # current_index = state_to_index(state, num_states)
    current_q_value = q_table[current_index][action]

    next_state_index = state_to_index(next_state, num_states)
    
    ## Finding the argmax Q value for next state
    next_state_q_value = np.max(q_table[next_state_index])

    updated_q_value = current_q_value + alpha * (reward + gamma * next_state_q_value - current_q_value)

    q_table[current_index][action] = updated_q_value

    return q_table

def save_q_table_as_csv(q_table):
    np.savetxt("q_table.csv", q_table, delimiter=",")

def load_q_table(filename="q_table.csv"):
    return np.loadtxt(filename, delimiter=",")