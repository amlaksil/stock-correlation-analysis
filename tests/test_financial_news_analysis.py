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
import pycodestyle
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


sample_data = pd.DataFrame({
    'headline': [
        'Stocks That Hit 52-Week Highs On Friday',
        'Stocks That Hit 52-Week Highs On Wednesday',
        '71 Biggest Movers From Friday'],
    'url': [
        'https://www.benzinga.com/news/20/06/16190091/' +
        'stocks-that-hit-52-week-highs-on-friday',
        'https://www.benzinga.com/news/20/06/16170189/' +
        'stocks-that-hit-52-week-highs-on-wednesday',
        'https://www.benzinga.com/news/20/05/16103463/' +
        '71-biggest-movers-from-friday'],
    'publisher': [
        'Benzinga Insights',
        'Benzinga Insights',
        'Lisa Levin'],
    'date': [
        '2020-06-05 10:30:54-04:00',
        '2020-06-03 10:45:20-04:00',
        '2020-05-26 04:30:07-04:00'],
    'stock': ['A', 'A', 'A']
})


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
        headline_stats, publisher_counts, date_counts = \
            self.financial_news_analysis.descriptive_statistics()

        # Check headline_stats
        self.assertAlmostEqual(int(headline_stats['count']), 100)
        self.assertAlmostEqual(round(headline_stats['mean'], 2), 95.05)
        self.assertAlmostEqual(round(headline_stats['std'], 2), 64.45)
        self.assertEqual(headline_stats['min'], 29)
        self.assertEqual(int(headline_stats['max']), 304)

        # Check publisher_counts
        self.assertEqual(publisher_counts['Benzinga Newsdesk'], 41)
        self.assertEqual(publisher_counts['Lisa Levin'], 28)
        self.assertEqual(publisher_counts['Vick Meyer'], 11)
        self.assertEqual(publisher_counts['Wayne Duggan'], 3)
        self.assertEqual(publisher_counts['Tyree Gorges'], 2)
        self.assertEqual(publisher_counts['Joel Elconin'], 1)

        # Check publish date counts
        date_counts.index = pd.to_datetime(date_counts.index)
        self.assertEqual(date_counts['2020-05-22'], 7)
        self.assertEqual(date_counts['2020-06-05'], 1)
        self.assertEqual(date_counts['2020-06-03'], 1)
        self.assertEqual(date_counts['2020-05-26'], 1)

    @patch('src.financial_news_analysis.pd.read_csv')
    def test_descriptive_statistics_mock(self, mock_read_csv):
        """Test descriptive_statistics method"""
        # Mock pd.read_csv with the sample data
        mock_read_csv.return_value = sample_data
        fns = FinancialNewsAnalysis(None)
        headline_stats, publisher_counts, date_counts = \
            fns.descriptive_statistics()

        # Assertions based on the sample data
        self.assertAlmostEqual(int(headline_stats['count']), 3)
        self.assertAlmostEqual(round(headline_stats['mean'], 2), 36.67)
        self.assertAlmostEqual(round(headline_stats['std'], 2), 6.81)
        self.assertEqual(headline_stats['min'], 29)
        self.assertEqual(int(headline_stats['max']), 42)

        # Assert publisher counts based on sample data
        self.assertEqual(publisher_counts['Benzinga Insights'], 2)
        self.assertEqual(publisher_counts['Lisa Levin'], 1)

        date_counts.index = pd.to_datetime(date_counts.index)
        self.assertEqual(date_counts['2020-06-05'], 1)
        self.assertEqual(date_counts['2020-06-03'], 1)
        self.assertEqual(date_counts['2020-05-26'], 1)

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
