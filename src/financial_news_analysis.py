#!/usr/bin/python3
"""
This module provides a class, FinancialNewsAnalysis, for performing
descriptive statistics analysis on financial news data.
"""
import pandas as pd
import matplotlib.pyplot as plt


class FinancialNewsAnalysis:
    """
    A class for analyzing financial news data.

    Parameters:
    - data_path (str): The path to the CSV file containing the financial
    news data.
    """
    def __init__(self, data_path):
        """
        Initialize the FinancialNewsAnalysis object.

        Args:
        - data_path (str): The path to the CSV file containing the financial
        news data.
        """
        self.data = pd.read_csv(data_path)

    def descriptive_statistics(self):
        """
        Perform descriptive statistics analysis on the financial news data.

        Returns:
        - headline_stats (pandas Series): Basic statistics for headline lengths
        - publisher_counts (pandas Series): Number of articles per publisher.
        - date_counts (pandas Series): Number of articles published on each
        date.
        """
        # Calculate headline lengths
        self.data['headline_length'] = self.data['headline'].apply(len)

        # Basic statistics for headline lengths
        headline_stats = self.data['headline_length'].describe()

        # Count number of articles per publisher
        publisher_counts = self.data['publisher'].value_counts()

        # Analyze publication dates
        self.data['date'] = pd.to_datetime(self.data['date'], errors='coerce')
        date_counts = self.data['date'].dt.date.value_counts()

        return headline_stats, publisher_counts, date_counts

    def visualize_stat_measures(self):
        """
        Visualize descriptive statistics measures.

        This method generates and displays visualizations for descriptive
        statistics of the dataset.
        It includes a histogram of headline lengths, a bar plot of the top 10
        publishers by article count,
        and a histogram of publication dates.

        Returns:
            None
        """
        # Headline Length Histogram
        plt.figure(figsize=(12, 6))
        plt.hist(
            self.data['headline_length'],
            bins=30, color='skyblue', edgecolor='black')
        plt.xlabel('Headline Length')
        plt.ylabel('Frequency')
        plt.title('Distribution of Headline Lengths')
        plt.grid(axis='y', alpha=0.75)
        plt.show()

        # Publisher Article Counts Bar Plot
        plt.figure(figsize=(14, 6))
        publisher_counts = self.data['publisher'].value_counts()
        # Displaying only top 10 publishers for better visibility
        top_publishers = publisher_counts.head(10)
        top_publishers.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.xlabel('Publisher')
        plt.ylabel('Number of Articles')
        plt.title('Top 10 Publishers by Article Count')
        plt.xticks(rotation=45, ha='right')
        plt.show()

        # Publication Date Counts Histogram
        plt.figure(figsize=(12, 6))
        # To remove 'NaT' values from the data['date'] use dropna()
        plt.hist(
            self.data['date'].dropna(),
            bins=50, color='skyblue', edgecolor='black')
        plt.xlabel('Publication Date')
        plt.ylabel('Frequency')
        plt.title('Publication Date Distribution')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.75)
        plt.show()
