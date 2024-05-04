#!/usr/bin/python3
"""
This module contains a class called `TimeSeriesAnalysis` that
analyzes time series data of financial news articles.
"""
import matplotlib.pyplot as plt
import pandas as pd
from src.financial_news_analysis import FinancialNewsAnalysis


class TimeSeriesAnalysis(FinancialNewsAnalysis):
    """
    A class for analyzing time series data of financial news articles.

    Attributes:
    - data_path (str): The path to the dataset CSV file.
    - data (DataFrame): The DataFrame containing the financial news data.
    """

    def publication_frequency_over_time(self):
        """
        Calculate the publication frequency of articles over time.

        Returns:
        - publication_frequency (pd.Series): A pandas Series with the
        publication frequency for each date.
        """
        # Convert 'date' column to datetime
        self.data['date'] = pd.to_datetime(self.data['date'], errors='coerce')

        # Group by date and count the number of articles published each day
        publication_frequency = self.data.groupby(
            self.data['date'].dt.date).size()

        return publication_frequency

    def plot_publication_frequency(self, publication_frequency):
        """
        Plot the publication frequency over time.

        Args:
        - publication_frequency (pd.Series): A pandas Series with the
        publication frequency for each date.
        """
        plt.figure(figsize=(15, 6))
        publication_frequency.plot(kind='line')
        plt.title('Publication Frequency Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles Published')
        plt.grid(True)
        plt.show()

    def analyze_publication_times(self):
        """
        Analyzes the distribution of publication times throughout the day.
        Plots a bar chart showing the number of articles published in
        each hour.
        """
        # Extract the hour component from the 'date' column
        self.data['hour'] = self.data['date'].dt.hour

        # Group by hour and count the number of articles published in each hour
        publication_times = self.data.groupby('hour').size()

        # Plotting publication times
        plt.figure(figsize=(12, 6))
        publication_times.plot(kind='bar')
        plt.title('Publication Times Analysis')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Articles Published')
        plt.xticks(rotation=0)
        plt.show()

    def analyze_article_spikes(self):
        """
        Identifies spikes in article publications related to specific
        market events.
        Plots the publication frequency over time, highlighting the spikes.
        """
        # Calculate daily publication frequency
        daily_publication_frequency = self.data.groupby(
            self.data['date'].dt.date).size()

        # Calculate the mean and standard deviation of daily
        # publication frequency
        mean_publication = daily_publication_frequency.mean()
        std_dev_publication = daily_publication_frequency.std()

        # Find spikes where the publication frequency is above
        # the mean + 2 standard deviations
        spikes = daily_publication_frequency[daily_publication_frequency > (
            mean_publication + 2 * std_dev_publication)]

        # Plot the spikes
        plt.figure(figsize=(15, 6))
        daily_publication_frequency.plot(kind='line')
        spikes.plot(
            marker='o', linestyle='', color='r', markersize=8, label='Spikes')
        plt.title('Publication Frequency with Spikes')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles Published')
        plt.legend()
        plt.grid(True)
        plt.show()
