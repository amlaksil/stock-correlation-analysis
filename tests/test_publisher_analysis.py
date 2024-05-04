#!/usr/bin/python3
"""
This module contains tests for `PublisherAnalysis` analysis class.
"""
import unittest
import inspect
from unittest.mock import patch
import pandas as pd
import pycodestyle
from src.publisher_analysis import PublisherAnalysis
import src

MODULE_DOC = src.publisher_analysis.__doc__

def check_docstring(func):
    """
    Ensures the provided function has a docstring.

    Args:
        func: The function to check.

    Raises:
        AssertionError: If the function doesn't have a docstring.
    """
    assert func.__doc__ is not None, f"{func[0]} method needs a docstring"
    assert len(func.__doc__) > 1, f"{func[0]} method needs a docstring"


class TestPublisherAnalysisDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of TimeSeriesAnalysis
    class.
    """
    def setUp(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(
            PublisherAnalysis, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that src/publisher_analysis.py conforms to PEP8."""
        for path in ['src/publisher_analysis.py',
                     'tests/test_publisher_analysis.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(MODULE_DOC, None,
                         "publisher_analysis.py needs a docstring")
        self.assertTrue(len(MODULE_DOC) > 1,
                        "publisher_analysis.py needs a docstring")

    def test_class_docstring(self):
        """Test for the PublisherAnalysis class docstring"""
        self.assertIsNot(PublisherAnalysis.__doc__, None,
                         "PublisherAnalysis class needs a docstring")
        self.assertTrue(len(PublisherAnalysis.__doc__) >= 1,
                        "PublisherAnalysis class needs a docstring")

    def test_func_docstrings(self):
        """
        Test for the presence of docstrings in PublisherAnalysis methods.
        """
        for func in self.base_funcs:
            with self.subTest(function=func):
                check_docstring(func[1])


class TestPublisherAnalysis(unittest.TestCase):
    """
    A class for testing the PublisherAnalysis class methods.
    """

    def setUp(self):
        """
        Set up a sample DataFrame for testing.
        """
        data = {
            'publisher': [
                'publisher1@example.com',
                'publisher2@example.com',
                'publisher1@example.com', 'publisher3@example.com'],
            'headline': [
                'Headline 1', 'Headline 2', 'Headline 3', 'Headline 4'],
            'date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-03']
        }
        self.df = pd.DataFrame(data)

    def test_top_publishers(self):
        """
        Test the top_publishers method.
        """
        publisher_analysis = PublisherAnalysis('data/raw_analyst_ratings.csv')
        publisher_analysis.data = self.df

        top_publishers = publisher_analysis.top_publishers(2)
        self.assertEqual(len(top_publishers), 2)
        self.assertEqual(
            top_publishers.index.tolist(),
            ['publisher1@example.com', 'publisher2@example.com'])
        self.assertEqual(top_publishers.values.tolist(), [2, 1])

    def test_extract_domains(self):
        """
        Test the extract_domains method.
        """
        publisher_analysis = PublisherAnalysis('data/raw_analyst_ratings.csv')
        publisher_analysis.data = self.df

        publisher_domains = publisher_analysis.extract_domains()
        self.assertEqual(publisher_domains.tolist(), [
            'example', 'example', 'example', 'example'])

    def test_invalid_data_path(self):
        """Test handling of invalid data path"""
        # Test if an invalid data path raises an exception
        with self.assertRaises(FileNotFoundError):
            PublisherAnalysis('invalid_path_to_data.csv')

    def test_plot_publisher_distribution(self):
        """
        Test if plot_publication_frequency produces expected output
        """
        # Define top_publishers
        top_publishers = pd.Series(
                [1, 2, 3], index=pd.Index(
                    ['Publisher A', 'Publisher B', 'Publisher C'],
                    name='Publisher'))
        with patch('src.publisher_analysis.plt.show') as mock_show:
            publisher_analysis = PublisherAnalysis(
                'data/raw_analyst_ratings.csv')
            publisher_analysis.plot_publisher_distribution(
                top_publishers)
            mock_show.assert_called()


if __name__ == '__main__':
    unittest.main()
