#!/usr/bin/python3
"""
This module provides the TimeSeriesAnalysis class for analyzing financial
news data.
"""
from datetime import datetime
from unittest.mock import patch
import unittest
import inspect
import pandas as pd
import pycodestyle
from src.time_series_analysis import TimeSeriesAnalysis
import src
MODULE_DOC = src.time_series_analysis.__doc__


class TestTimeSeriesAnalysisDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of TimeSeriesAnalysis
    class.
    """
    def setUp(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(
            TimeSeriesAnalysis, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that src/time_series_analysis.py conforms to PEP8."""
        for path in ['src/time_series_analysis.py',
                     'tests/test_time_series_analysis.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(MODULE_DOC, None,
                         "time_series_analysis.py needs a docstring")
        self.assertTrue(len(MODULE_DOC) > 1,
                        "time_series_analysis.py needs a docstring")

    def test_class_docstring(self):
        """Test for the TimeSeriesAnalysis class docstring"""
        self.assertIsNot(TimeSeriesAnalysis.__doc__, None,
                         "TimeSeriesAnalysis class needs a docstring")
        self.assertTrue(len(TimeSeriesAnalysis.__doc__) >= 1,
                        "TimeSeriesAnalysis class needs a docstring")

    def test_func_docstrings(self):
        """
        Test for the presence of docstrings in TimeSeriesAnalysis methods.
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
    """Unit tests for TimeSeriesAnalysis class"""
    def setUp(self):
        """
        Set up test data and create an instance of FinancialNewsAnalysis.
        """
        self.data_path = 'data/raw_analyst_ratings.csv'
        self.time_series_analysis = TimeSeriesAnalysis(self.data_path)

    @patch('src.time_series_analysis.pd.read_csv')
    def test_init(self, mock_read_csv):
        """
        Test if __init__ initializes the class with the provided data path
        """
        self.time_series_analysis = TimeSeriesAnalysis(None)
        mock_read_csv.assert_called_once_with(None)

    def test_publication_frequency_over_time(self):
        """
        Test if publication_frequency_over_time produces expected output
        """
        # Create a mock DataFrame with 'date' column
        dates = [
            '2022-01-01',
            '2022-01-01', '2022-01-02', '2022-01-02', '2022-01-02']
        df = pd.DataFrame({'date': dates})

        with patch.object(
                pd, 'to_datetime',
                return_value=pd.Series(
                    [datetime(2022, 1, 1),
                     datetime(2022, 1, 2)] * 3)) as _:
            self.time_series_analysis.data = df
            publication_frequency = \
                self.time_series_analysis.publication_frequency_over_time()
            expected_result = pd.Series(
                [3, 2], index=[datetime(2022, 1, 1), datetime(2022, 1, 2)])
            self.assertTrue(publication_frequency.equals(expected_result))

    def test_invalid_data_path(self):
        """Test handling of invalid data path"""
        # Test if an invalid data path raises an exception
        with self.assertRaises(FileNotFoundError):
            TimeSeriesAnalysis('invalid_path_to_data.csv')

    def test_plot_publication_frequency(self):
        """
        Test if plot_publication_frequency produces expected output
        """
        publication_frequency = pd.Series(
            [1, 2, 3], index=pd.date_range('2022-01-01', periods=3))
        with patch('src.time_series_analysis.plt.show') as mock_show:
            self.time_series_analysis.plot_publication_frequency(
                publication_frequency)
            mock_show.assert_called()

    def test_analyze_publication_times(self):
        """
        Test if analyze_publication_times produces expected output
        """
        # Create a mock DataFrame with 'date' column
        df = pd.DataFrame(
            {'date': pd.date_range('2022-01-01', periods=3, freq='H')})
        self.time_series_analysis.data = df
        with patch('src.time_series_analysis.plt.show') as mock_show:
            self.time_series_analysis.analyze_publication_times()
            mock_show.assert_called()

    def test_analyze_article_spikes(self):
        """
        Test if analyze_article_spikes produces expected output
        """
        # Create a mock DataFrame with 'date' column
        dates = pd.date_range('2022-01-01', periods=10)
        frequencies = [10, 12, 8, 20, 25, 6, 7, 18, 30, 8]
        df = pd.DataFrame({'date': dates, 'frequency': frequencies})
        self.time_series_analysis.data = df

        with patch('src.time_series_analysis.plt.show') as mock_show:
            self.time_series_analysis.analyze_article_spikes()
            mock_show.assert_called()


if __name__ == '__main__':
    unittest.main()
