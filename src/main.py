"""
Created: 7/28/2024

AUTHOR: JGERMANN
"""

from training import ActivityManager
from alien_invasion import Game

show_scoreboard = False
debug = False
training = True

# Q Table
load_q_table = False # Load Q Table at startup
save_q_table = False # Saves Q Table upon closing window

render_game = False

# Activity Manager class params
save_data = False
show_data = True

"""
Start the main game
"""
def main():
    if training:
        manager = ActivityManager(save_data, show_data)
        game = Game(show_scoreboard, debug, manager, save_q_table, load_q_table, render_game)
    else:
        game = Game(show_scoreboard, debug)

    game.run_game()

if __name__ == '__main__':
    main()