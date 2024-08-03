"""
Created Sun Jul 28 10:00:00 2024

@author: JGERMANN
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

""" 
    Management class that tracks and displays general performance metrics, save/load existing models, 
    and run the game in a training mode.
"""
class ActivityManager():
    
    """Initializing function."""
    def __init__(self, show_data = False):
        
        self.show_data = show_data
        self.max_epochs = 5
        self.num_epochs = 0
        self.scores = list()
    
    def show_performance_data(self):
        epoch_list = list()
        score_list = list()
        if len(self.scores) != 0:
            for pair in self.scores:
                epoch_list.append(pair[0])
                score_list.append(pair[1])
            plt.plot(epoch_list, score_list)
            plt.show()
        else:
            print("No data to show!")
    
    """Store the final score for the current epoch."""
    def finish_epoch(self, epoch_score):
        self.scores.append(np.array([self.num_epochs, epoch_score]))
        self.num_epochs += 1
        