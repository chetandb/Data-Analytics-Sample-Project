import pytest
import pandas as pd
from Aggregator import Aggregator

@pytest.fixture
def sample_df():
    data = {
        'user_id': [1, 2, 1, 2, 1, 3],
        'amount': [100, 200, 150, 300, 50, 400],
        'age': [25, 30, 25, 40, 25, 35]
    }
    return pd.DataFrame(data)

def test_calculate_aggregated_values_sum(sample_df):
    aggregator = Aggregator(sample_df)
    calculations = {'amount': 'sum', 'age': 'mean'}
    aggregated_df = aggregator.calculate_aggregated_values(['user_id'], calculations)

    # Ensure aggregation is correct
    expected_data = {
        'user_id': [1, 2, 3],
        'amount': [300, 500, 400],
        'age': [25.0, 35.0, 35.0]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(aggregated_df, expected_df)

def test_calculate_aggregated_values_mean(sample_df):
    aggregator = Aggregator(sample_df)
    calculations = {'amount': 'mean', 'age': 'mean'}
    aggregated_df = aggregator.calculate_aggregated_values(['user_id'], calculations)

    # Ensure aggregation is correct
    expected_data = {
        'user_id': [1, 2, 3],
        'amount': [100.0, 250.0, 400.0],
        'age': [25.0, 35.0, 35.0]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(aggregated_df, expected_df)

def test_calculate_aggregated_values_custom_agg(sample_df):
    aggregator = Aggregator(sample_df)
    calculations = {'amount': lambda x: x.max() - x.min(), 'age': 'mean'}
    aggregated_df = aggregator.calculate_aggregated_values(['user_id'], calculations)

    # Ensure custom aggregation is correct
    expected_data = {
        'user_id': [1, 2, 3],
        'amount': [100, 100, 0],
        'age': [25.0, 35.0, 35.0]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(aggregated_df, expected_df)

if __name__ == '__main__':
    pytest.main()
