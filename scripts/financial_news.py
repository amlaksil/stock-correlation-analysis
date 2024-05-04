#!/usr/bin/python3
from src.financial_news_analysis import FinancialNewsAnalysis
if __name__ == '__main__':
    data_path = 'data/raw_analyst_ratings.csv'
    financial_news_analysis = FinancialNewsAnalysis(data_path)
    headline_stats, publisher_counts, date_counts = \
        financial_news_analysis.descriptive_statistics()
    print("Headline Length Statistics:")
    print(headline_stats)
    print("\nPublisher Article Counts:")
    print(publisher_counts)
    print("\nPublication Date Analysis:")
    print(date_counts)
    financial_news_analysis.visualize_stat_measures()
