from training import Training
from alien_invasion import Game

show_scoreboard = False
debug = False
"""
Start the main game
"""
def main():
    game = Game(show_scoreboard, debug)
    game.run_game()


if __name__ == '__main__':
    main()