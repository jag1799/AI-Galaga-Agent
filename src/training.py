"""
Created Sun Jul 28 10:00:00 2024

@author: JGERMANN
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pygame

""" 
    Management class that tracks and displays general performance metrics, save/load existing models, 
    and run the game in a training mode.
"""
class ActivityManager():
    
    """Initializing function."""
    def __init__(self, show_data = False):
        self.show_data = show_data
        self.max_epochs = 50
        self.num_epochs = 0
        self.scores = list()
        self.scores_value=list()
        self.train_rewards = []
        self.event_counts = []
        
    def update_metrics(self, ai_settings):
        """Update the tracked metrics from the ai_settings."""
        self.train_rewards.append(ai_settings.train_reward)
        self.event_counts.append(ai_settings.event_count)

    def show_training_reward_data(self):
        if len(self.train_rewards) == 0 or len(self.event_counts) == 0:
            print("No data to show!")
            return
    
        event_count_array = np.array(self.event_counts)
        train_rewards_array = np.array(self.train_rewards)
        
        normalized_reward = train_rewards_array/event_count_array
    
        epoch_list = list(range(len(normalized_reward)))
        
        # Plot normalized rewards per epoch
        plt.figure(figsize=(12, 6))
        plt.plot(epoch_list, normalized_reward, label='Normalized Reward')
        
        # Calculate the regression line
        epoch_array = np.array(epoch_list)

        if len(epoch_array) > 1:  # Ensure there are enough points for regression
            slope, intercept = np.polyfit(epoch_array, normalized_reward, 1)
            regression_line = slope * epoch_array + intercept
            
            # Calculate R^2 value
            ss_res = np.sum((normalized_reward - regression_line) ** 2)
            ss_tot = np.sum((normalized_reward - np.mean(normalized_reward)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            print(f'The r^2 value is: {r_squared}')
            print(f'The slope is: {slope}')
            
            plt.plot(epoch_list, regression_line, color='red', label='Regression Line')
        
        # Determine tick interval
        min_epoch = min(epoch_list) if epoch_list else 0
        max_epoch = max(epoch_list) if epoch_list else 0
        range_span = max_epoch - min_epoch
        if range_span > 0:
            if range_span < 200:
                tick_interval = 10
            elif range_span < 500:
                tick_interval = 50
            elif range_span < 1000:
                tick_interval = 100
            else:
                tick_interval = 250
            ticks = np.arange(min_epoch, max_epoch + tick_interval, tick_interval)
            plt.xticks(ticks=ticks)
        
        plt.xlabel('Epoch')
        plt.ylabel('Normalized Reward')
        plt.title('Normalized Reward vs. Epoch')
        plt.legend()
        plt.show()

    """Display the performance data of actual scores vs. epochs."""
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
            # Clean data
            epoch_array = [np.isfinite(epoch_array)]
            print(score_array)
            score_array = [np.isfinite(score_array)]

            try:
                # Check for NaNs or Infs in data
                if np.any(np.isnan(epoch_array)) or np.any(np.isnan(score_array)):
                    raise ValueError("Data contains NaNs")
                if np.any(np.isinf(epoch_array)) or np.any(np.isinf(score_array)):
                    raise ValueError("Data contains Infs")
            
                # Calculate the regression line
                slope, intercept = np.polyfit(epoch_array, score_array, 1)
                regression_line = slope * epoch_array + intercept
                
                # Calculate R^2 value
                ss_res = np.sum((score_array - regression_line) ** 2)
                ss_tot = np.sum((score_array - np.mean(score_array)) ** 2)
                r_squared = 1 - (ss_res / ss_tot)
                print(f'The r^2 value is :{r_squared}')
                print(f'The slope is :{slope}')
                
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
            except np.linalg.LinAlgError as e:
                print(f'LinAlgError: {e}')
            except ValueError as e:
                print(f'ValueError: {e}')
            except Exception as e:
                print(f'Unexpected error: {e}')
        
        else:
            print("No data to show!")
    
    """Store the final score for the current epoch."""
    def finish_epoch(self, epoch_score,ai_settings):
        self.scores.append(np.array([self.num_epochs, epoch_score]))
        self.scores_value.append(epoch_score)
        self.num_epochs += 1
        self.update_metrics(ai_settings)

        if self.num_epochs == self.max_epochs:
            if hasattr(self, 'activity_manager') and self.activity_manager:
                self.activity_manager.game_active = False

            pygame.event.post(pygame.event.Event(pygame.QUIT))