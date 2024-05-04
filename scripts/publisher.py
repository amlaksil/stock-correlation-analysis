#!/usr/bin/python3
from sys import argv
from src.publisher_analysis import PublisherAnalysis
if __name__ == '__main__':
    if len(argv) > 1:
        data_path = argv[1]
        publisher_analysis = PublisherAnalysis(data_path)
        top_publishers = publisher_analysis.top_publishers()
        publisher_analysis.plot_publisher_distribution(top_publishers)

        publisher_domains = publisher_analysis.extract_domains()
        unique_domains = publisher_domains.unique()
        print("Unique Publisher Domains:")
        print(unique_domains)
