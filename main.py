"""
Created: 7/28/2024

AUTHOR: JGERMANN
"""


from training import ActivityManager
from alien_invasion import Game

show_scoreboard = True
debug = False
training = True

# Activity Manager class params
show_data = True

"""
Start the main game
"""
def main():
    if training:
        manager = ActivityManager(show_data)
        game = Game(show_scoreboard, debug, manager)
    else:
        game = Game(show_scoreboard, debug)

    game.run_game()
    print("Here")

if __name__ == '__main__':
    main()