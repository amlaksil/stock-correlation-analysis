#!/usr/bin/python3
"""
This module contains a class called `PublisherAnalysis` which
analyze publishers in the financial news dataset
"""
import tldextract
import matplotlib.pyplot as plt
from src.financial_news_analysis import FinancialNewsAnalysis


class PublisherAnalysis(FinancialNewsAnalysis):
    """
    A class for analyzing publishers in the financial news dataset.

    Inherits from FinancialNewsAnalysis for access to dataset and basic
    analysis methods.
    """
    def top_publishers(self, n=10):
        """
        Calculate the top publishers contributing to the news feed.

        Parameters:
        - n (int): Number of top publishers to return.

        Returns:
        - pandas Series: Top publishers and the number of articles
        published by each.
        """
        top_publishers = self.data['publisher'].value_counts().head(n)
        return top_publishers

    def extract_domains(self):
        """
        Extract unique domains from email addresses used as publisher names.

        Returns:
        - pandas Series: Unique domains extracted from publisher email
        addresses.
        """
        def extract_domain(email):
            """
            Extract the domain from an email address.

            Args:
                - email (str): Email address from which to extract the domain.

            Returns:
                - str: Extracted domain from the email address.
            """
            ext = tldextract.extract(email)
            return ext.domain

        self.data['publisher_domain'] = self.data['publisher'].apply(
            extract_domain)
        return self.data['publisher_domain']

    def plot_publisher_distribution(self, top_publishers):
        """
        Plot the distribution of publishers based on the number of articles
        published.

        Args:
        - top_publishers (pandas Series): Top publishers and the number of
        articles published by each.
        """
        plt.figure(figsize=(12, 6))
        top_publishers.plot(kind='bar')
        plt.title('Top Publishers')
        plt.xlabel('Publisher')
        plt.ylabel('Number of Articles Published')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()
