"""
Created: 7/28/2024

AUTHOR: JGERMANN
"""


from training import ActivityManager
from alien_invasion import Game


###############################################################################
## User settings to adjust
training = False
render_game = False
show_scoreboard = False
###############################################################################

# Q_table 
load_q_table = False # load Q_table at startup
save_q_table = False # saves Q table upon closing window
index_log=[]

# Activity Manager class params
show_data = True

"""
Start the main game
"""
def main():
    if training:
        manager = ActivityManager(show_data)
        game = Game(show_scoreboard, manager, save_q_table, load_q_table, render_game, index_log, training)
    else:
        manager = ActivityManager(show_data)
        game = Game(show_scoreboard, manager, save_q_table, load_q_table, render_game, index_log, training)

    log = game.run_game()

    return log

if __name__ == '__main__':
    log2 = main()