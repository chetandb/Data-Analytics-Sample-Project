import pytest
import pandas as pd
import numpy as np
from DataCleaner import DataCleaner  # Adjust import based on your file structure

# Sample data for testing
@pytest.fixture
def sample_df():
    data = {
        'A': [1, 2, np.nan, 4],
        'B': [np.nan, np.nan, 3, 4],
        'C': ['foo', 'bar', 'baz', np.nan]
    }
    return pd.DataFrame(data)

def test_handle_missing_values_mean(sample_df):
    cleaner = DataCleaner(sample_df.copy())
    cleaned_df = cleaner.handle_missing_values(strategy='mean')
    assert cleaned_df['A'].isna().sum() == 0
    assert cleaned_df['B'].isna().sum() == 0
    assert cleaned_df['C'].isna().sum() == 1  # No mean for non-numeric columns

def test_handle_missing_values_median(sample_df):
    cleaner = DataCleaner(sample_df.copy())
    cleaned_df = cleaner.handle_missing_values(strategy='median')
    assert cleaned_df['A'].isna().sum() == 0
    assert cleaned_df['B'].isna().sum() == 0
    assert cleaned_df['C'].isna().sum() == 1  # No median for non-numeric columns
