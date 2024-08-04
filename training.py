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
    def __init__(self, save_data = False):
        
        self.save_data = save_data
        self.max_epochs = 3
        self.num_epochs = 0
        self.scores = list()
    
    """Store the epoch-score performance data in a csv file for later usage."""
    def save_performance_data(self):
        if len(self.scores) > 0:
            df = pd.DataFrame(self.scores, columns=['Epoch', 'Score'])
            df.to_csv("~/Documents/vscode_ws/GalagaAI/performance.csv", index=False)
        else:
            print("No data to write!")
    
    """Store the final score for the current epoch."""
    def finish_epoch(self, epoch_score):
        self.scores.append(np.array([self.num_epochs, epoch_score]))
        self.num_epochs += 1
        