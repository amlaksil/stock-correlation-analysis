#!/usr/bin/python3
from src.time_series_analysis import TimeSeriesAnalysis
if __name__ == '__main__':
    data_path = '~/stock/raw_analyst_ratings.csv'
    time_series_analysis = TimeSeriesAnalysis(data_path)
    publication_frequency = time_series_analysis.publication_frequency_over_time()
    time_series_analysis.plot_publication_frequency(publication_frequency)
    time_series_analysis.analyze_publication_times()
    time_series_analysis.analyze_article_spikes()
