"""
Created Sun Jul 28 10:00:00 2024

@author: JGERMANN
"""

from alien_invasion import Game

class Training():
    """
    Training instance controller that oversees the
    performance of the agent and the number of epochs
    elapsed.
    """
    def __init__(self):
        self.epoch_num = 0
        
    def start_training(self):
        epoch = Epoch()
    def update_training_records(self):
        self.epoch_num += 1

class Epoch():

    """
    A single alien invasion training instance within 
    a Training() object
    """
    def __init__(self):
        pass
    
    """
    Run a single game instance until a failure condition is reached.
    This condition will always be the agent loses all its lives.
    """
    def run_epoch(self):
        pass