# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 10:15:51 2024

@author: PFINN
"""

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
# import alien_invasion as alin

import numpy as np
import random
import hashlib


def get_state(ship : Ship,aliens,alien_bullets):

    ## Ship position
    ship_center = (ship.center-50)//100 # x-position 0 to 9

    ## alien positions 
    alien_x_columns = np.zeros(10,dtype = int)
    lowest_alien_y = 0
    for alien in aliens:
        # gathering alien x,y info
        x_pixel,y_pixel =alien.x//100,alien.rect.y //100 
        # placing alien x info into a 1 for presence in a column
        alien_x_columns[x_pixel] = 1
        
        lowest_alien_y = max(lowest_alien_y,y_pixel)
        
    ## convery alien_x_columns to an integer
    binary_string = ''.join(map(str,alien_x_columns))
    alien_x_columns_int = int(binary_string,2)
    
    # Alien bullet position
    alien_bullet_min_y = None
    alien_bullet_min_x = None
    if alien_bullets:
        # Find the bullet with the maximum y position
        max_bullet = max(alien_bullets.sprites(), key=lambda bullet: bullet.rect.y)
        alien_bullet_min_y = (max_bullet.rect.y + 15) // 100 - 1
        alien_bullet_min_x = max_bullet.rect.x // 100
    
    # Sense outward two squares from the ship.  If there's a bullet, trigger flag in the state.
    bullet_detected : float = 0

    if ((ship.rect.centery + 15) // 100-1) + 2 == alien_bullet_min_y:
        print("Bullet detected at 2!")
        bullet_detected = 2
    elif ((ship.rect.centery + 15) // 100-1) + 1 == alien_bullet_min_y:
        print("Bullet detected at 1!")
        bullet_detected = 1
    

    state = (ship_center,alien_x_columns_int,lowest_alien_y,alien_bullet_min_y,alien_bullet_min_x, bullet_detected)

    # print(f'ship_center: {ship_center}')
    # print(f'alien_x_columns: {alien_x_columns}')
    # print(f'alien_x_columns_int: {alien_x_columns_int}')
    # print(f'lowest_alien_y: {lowest_alien_y}')
    # print(f'Alien bullet minimum Y: {alien_bullet_min_y}')
    # print(f'Alien bullet minimum X: {alien_bullet_min_x}')



    return state

def perform_action(action, ai_settings, ship, screen, bullets, stats, sb,alien_bullets,aliens):
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
    
    gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
    ship.update()
    return ship.rect.centerx


def initialize_q_table(num_states,num_actions):

    q_table = np.zeros((num_states,num_actions))

    return q_table

# convert state to index 
def state_to_index(state,num_states):
    # convert state to string
    state_str = str(state)
    
    #create stable hash
    hash_object = hashlib.sha256(state_str.encode())
    
    hash_int = int(hash_object.hexdigest(),16)
    state_index = hash_int % num_states

    return state_index


def choose_action(state,q_table,num_states):
    
    state_index = state_to_index(state,num_states)
    action_choice = np.argmax(q_table[state_index])
    
    return action_choice

def get_rewards(num_bullets,initial_lives,lives,initial_aliens,aliens_left, bullet_detected):
    
    reward = 0 
    
    # bullet component
    bullet_reward =-0.05*num_bullets
    
    # life component
    life_reward = (initial_lives-lives)*-1
    
    # aliens left reward
    aliens_left_reward = (initial_aliens-aliens_left)*.5

    bullet_detected_reward = bullet_detected * -0.25

    reward = bullet_reward + life_reward + aliens_left_reward + bullet_detected_reward
    
    return reward

def update_q_table(state,action, reward, next_state,alpha,gamma,num_states,q_table):
    
    #finding the row in the Q-table for the current state
    current_index = state_to_index(state, num_states)
    current_q_value = q_table[current_index][action]
    
    ## finding the argmax Q value for next state
    next_state_index = state_to_index(next_state, num_states)
    next_action = choose_action(next_state, q_table,num_states)
    next_state_q_value = q_table[next_state_index][next_action]

    updated_q_value = current_q_value+alpha* (reward+gamma*next_state_q_value-current_q_value)

    q_table[current_index][action]=updated_q_value

    return q_table


































































