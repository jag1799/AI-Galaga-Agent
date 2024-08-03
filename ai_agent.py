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
import random
import hashlib

"""Determine the current state status."""
def get_state(ship : Ship,aliens,alien_bullets):

    ## Ship position
    ship_center = (ship.center-50)//100 # x-position 0 to 9

    ## Alien positions 
    alien_x_columns = np.zeros(10,dtype = int)
    lowest_alien_y = 0
    for alien in aliens:
        # Gathering alien x,y info
        x_pixel,y_pixel =alien.x//100,alien.rect.y //100 
        # Placing alien x info into a 1 for presence in a column
        alien_x_columns[x_pixel] = 1
        
        lowest_alien_y = max(lowest_alien_y,y_pixel)
        
    ## Convert alien_x_columns to an integer
    binary_string = ''.join(map(str,alien_x_columns))
    alien_x_columns_int = int(binary_string,2)
    
    # Alien bullet position
    alien_bullet_min_y = None
    alien_bullet_min_x = None
    if alien_bullets:
        # Find the bullet with the maximum y position
        # NOTE: Y position increases the further down the screen an object is.
        max_bullet = max(alien_bullets.sprites(), key=lambda bullet: bullet.rect.y)
        alien_bullet_min_y = (max_bullet.rect.y + 15) // 100 - 1
        alien_bullet_min_x = max_bullet.rect.x // 100
    
    # Sense outward two squares from the ship.  If there's a bullet, trigger flag in the state.
    bullet_detected : float = 0

    # Get the square positioned 2 up and 1 right of the ship's current position.
    right_square : int = (((ship.rect.centerx // 100) + 1), (((ship.rect.centery + 15) // 100-1) - 2))

    # Get the square positioned 2 straight upward from the current ship position
    straight_square : int = (((ship.rect.centerx // 100)), (((ship.rect.centery + 15) // 100-1) - 2))

    # Get the square positioned 1 left and 2 up from the ship's current position.
    left_square : int = (((ship.rect.centerx // 100) - 1), (((ship.rect.centery + 15) // 100-1) - 2))

    # Scan the above calculated tiles for bullets
    if (right_square[0] == alien_bullet_min_x) and (right_square[1] == alien_bullet_min_y):
        bullet_detected = 1
    elif (straight_square[0] == alien_bullet_min_x) and (straight_square[1] == alien_bullet_min_y):
        bullet_detected = 2
    elif (left_square[0] == alien_bullet_min_x) and (left_square[1] == alien_bullet_min_y):
        bullet_detected = 1
    
    state = (ship_center,alien_x_columns_int,lowest_alien_y,alien_bullet_min_y,alien_bullet_min_x, bullet_detected)

    return state

"""Execute the agent selected action per the game rules."""
def perform_action(action, ai_settings, ship, screen, bullets, stats, sb,alien_bullets,aliens, activity_manager):
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
def initialize_q_table(num_states,num_actions):

    q_table = np.random.rand(num_states, num_actions)

    return q_table

"""Convert state to index."""
def state_to_index(state,num_states):
    # convert state to string
    state_str = str(state)
    
    #create stable hash
    hash_object = hashlib.sha256(state_str.encode())
    
    hash_int = int(hash_object.hexdigest(),16)
    state_index = hash_int % num_states

    return state_index

"""Select an action based on the current Q-Table."""
def choose_action(state,q_table,num_states):
    
    state_index = state_to_index(state,num_states)
    action_choice = np.argmax(q_table[state_index])
    
    return action_choice

"""Calculate the new overall reward."""
def get_rewards(num_bullets,initial_lives,lives,initial_aliens,aliens_left, bullet_detected):
    
    reward = 0
    
    # Reward pertaining to the number of bullets fired
    bullet_reward =-0.05*num_bullets
    
    # Reward pertaining to the number of lives lost
    life_reward = (initial_lives-lives)*-1
    
    # Reward pertaining to the number of aliens
    aliens_left_reward = (initial_aliens-aliens_left)*.5

    bullet_detected_reward = bullet_detected * -0.25

    reward = bullet_reward + life_reward + aliens_left_reward + bullet_detected_reward
    
    return reward

"""Update all relevant states within the Q-Table."""
def update_q_table(state,action, reward, next_state,alpha,gamma,num_states,q_table):
    
    # Finding the row in the Q-table for the current state
    current_index = state_to_index(state, num_states)
    current_q_value = q_table[current_index][action]
    
    ## Finding the argmax Q value for next state
    next_state_index = state_to_index(next_state, num_states)
    next_action = choose_action(next_state, q_table,num_states)
    next_state_q_value = q_table[next_state_index][next_action]

    updated_q_value = current_q_value+alpha* (reward+gamma*next_state_q_value-current_q_value)

    q_table[current_index][action]=updated_q_value

    return q_table


































































