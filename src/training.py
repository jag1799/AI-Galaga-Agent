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
    def __init__(self, save_data = False, show_data = False):
        
        self.show_data = show_data
        self.save_data = save_data
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
            # Calculate the range for x-axis ticks
            min_epoch = min(epoch_list) if epoch_list else 0
            max_epoch = max(epoch_list) if epoch_list else 0
            range_span = max_epoch - min_epoch
            
            epoch_array = np.array(epoch_list)
            score_array = np.array(score_list)
            
            
            # Calculate the regression line
            slope, intercept = np.polyfit(epoch_array, score_array, 1)
            regression_line = slope * epoch_array + intercept
            
            # Calculate R^2 value
            ss_res = np.sum((score_array - regression_line) ** 2)
            ss_tot = np.sum((score_array - np.mean(score_array)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            print(f'The r^2 value is :{r_squared}')
            
            # Plot the regression line
            plt.plot(epoch_list, regression_line, color='red', label='Regression Line')
            
            
            # Determine tick interval
            if range_span > 0:
                if range_span < 20:
                    tick_interval = 1
                elif range_span < 50:
                    tick_interval = 5
                elif range_span < 100:
                    tick_interval = 10
                else:
                    tick_interval = 25
            
            ticks = np.arange(min_epoch, max_epoch + tick_interval, tick_interval)
            plt.xticks(ticks=ticks)
            
            plt.xlabel('Epoch')
            plt.ylabel('Score')
            plt.title('Score vs. Epoch')
            plt.legend()
            
            plt.show()
        else:
            print("No data to show!")
            
    """Store the epoch-score performance data in a csv file for later usage."""
    def save_performance_data(self):
        if len(self.scores) > 0:
            df = pd.DataFrame(self.scores, columns=['Epoch', 'Score'])
            df.to_csv("performance.csv", index=False)
        else:
            print("No data to write!")
    
    """Store the final score for the current epoch."""
    def finish_epoch(self, epoch_score):
        self.scores.append(np.array([self.num_epochs, epoch_score]))
        self.num_epochs += 1
        