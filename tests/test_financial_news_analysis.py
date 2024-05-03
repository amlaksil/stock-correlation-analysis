#!/usr/bin/python3
"""
This module provides the FinancialNewsAnalysis class for analyzing financial
news data. The FinancialNewsAnalysis class allows users to load and analyze
data from a CSV file containing financial news data, including headlines, URLs
publishers, dates, and stock symbols. It provides methods for descriptive
statistics, handling missing values, and visualizing statistical measures.
"""
from unittest.mock import patch
import unittest
import inspect
import pandas as pd
import pep8 as pycodestyle
from src.financial_news_analysis import FinancialNewsAnalysis
import src
MODULE_DOC = src.financial_news_analysis.__doc__


class TestFinancialNewsAnalysisDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of FinancialNewsAnalysis
    class.
    """
    def setUp(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(
            FinancialNewsAnalysis, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that src/financial_news_analysis.py conforms to PEP8."""
        for path in ['src/financial_news_analysis.py',
                     'tests/test_financial_news_analysis.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(MODULE_DOC, None,
                         "financial_news_analysis.py needs a docstring")
        self.assertTrue(len(MODULE_DOC) > 1,
                        "financial_news_analysis.py needs a docstring")

    def test_class_docstring(self):
        """Test for the FinancialNewsAnalysis class docstring"""
        self.assertIsNot(FinancialNewsAnalysis.__doc__, None,
                         "FinancialNewsAnalysis class needs a docstring")
        self.assertTrue(len(FinancialNewsAnalysis.__doc__) >= 1,
                        "FinancialNewsAnalysis class needs a docstring")

    def test_func_docstrings(self):
        """
        Test for the presence of docstrings in FinancialNewsAnalysis methods.
        """
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    f"{func[0]} method needs a docstring"
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    f"{func[0]} method needs a docstring"
                )


class TestFinancialNewsAnalysis(unittest.TestCase):
    """Unit tests for FinancialNewsAnalysis class"""
    def setUp(self):
        """Set up test data and create an instance of FinancialNewsAnalysis"""
        self.data_path = 'data/raw_analyst_ratings.csv'
        self.financial_news_analysis = FinancialNewsAnalysis(self.data_path)

    @patch('src.financial_news_analysis.pd.read_csv')
    def test_initialization(self, mock_read_csv):
        """Test initialization of FinancialNewsAnalysis"""
        # Mock the pd.read_csv function to return a sample DataFrame
        sample_data = pd.DataFrame({
            'headline': ['headline1', 'headline2', 'headline3'],
            'url': ['url1', 'url2', 'url3'],
            'publisher': ['publisher1', 'publisher2', 'publisher3'],
            'date': ['2022-01-01', '2022-01-02', '2022-01-03'],
            'stock': ['AAPL', 'GOOGL', 'AMZN']
        })
        mock_read_csv.return_value = sample_data
        financial_news_analysis = FinancialNewsAnalysis(self.data_path)

        # Assert that pd.read_csv was called with the correct path
        mock_read_csv.assert_called_once_with(self.data_path)

        # Assert that data is loaded correctly
        self.assertIsNotNone(financial_news_analysis.data)
        self.assertEqual(len(financial_news_analysis.data), 3)
        # Check the length of the sample data

    def test_descriptive_statistics(self):
        """Test descriptive_statistics method"""
        headline_stats, publisher_counts, _ = \
            self.financial_news_analysis.descriptive_statistics()

        # Check headline_stats
        self.assertAlmostEqual(round(headline_stats['mean'], 2), 73.12)
        self.assertAlmostEqual(round(headline_stats['std'], 2), 40.74)
        self.assertEqual(headline_stats['min'], 3)
        self.assertEqual(int(headline_stats['max']), 512)

        # Check publisher_counts
        self.assertEqual(publisher_counts['Paul Quintaro'], 228373)
        self.assertEqual(publisher_counts['Lisa Levin'], 186979)
        self.assertEqual(publisher_counts['Benzinga Newsdesk'], 150484)
        self.assertEqual(publisher_counts['Charles Gross'], 96732)
        self.assertEqual(publisher_counts['Monica Gerson'], 82380)

    def test_invalid_data_path(self):
        """Test handling of invalid data path"""
        # Test if an invalid data path raises an exception
        with self.assertRaises(FileNotFoundError):
            FinancialNewsAnalysis('invalid_path_to_data.csv')

    def test_missing_values_handling(self):
        """Test handling of missing values"""
        # Test if missing values are handled correctly
        # Assuming a row with a missing headline in the CSV file
        missing_values_row = pd.DataFrame({
            'headline': [None],
            'url': ['url'],
            'publisher': ['publisher'],
            'date': ['2022-01-01'],
            'stock': ['stock']
        })
        with patch(
                'src.financial_news_analysis.pd.read_csv',
                return_value=missing_values_row):
            self.assertFalse(
                self.financial_news_analysis.data['headline'].isnull().any())

    def test_visualize_stat_measures_output(self):
        """
        Test if visualize_stat_measures produces expected output
        """
        self.financial_news_analysis.descriptive_statistics()
        with patch('src.financial_news_analysis.plt.show') as mock_show:
            self.financial_news_analysis.visualize_stat_measures()
            mock_show.assert_called()


if __name__ == '__main__':
    unittest.main()
