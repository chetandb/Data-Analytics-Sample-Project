from unittest.mock import MagicMock

import pandas as pd
import pytest

from DataPipeline import DataPipeline  # Adjust import based on your module name


@pytest.fixture
def sample_df():
    data = {
        'date': ['2024-01-01', '2024-01-02', None, '2024-01-04'],
        'user_id': [1, 2, 1, 2],
        'amount': [10, 20, 30, 40]
    }
    return pd.DataFrame(data)

def test_data_cleaning(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.data_cleaning()

    # Assert that missing values are forward filled
    assert pipeline.df['date'].isnull().sum() == 0
    # Assert duplicates are dropped (if any existed)
    assert len(pipeline.df) == len(sample_df.drop_duplicates())


def test_batch_process(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.data_cleaning()  # Clean data first
    pipeline.data_transformation()  # Transform data
    pipeline.batch_process(n_chunks=2)

    # Check if data is split into chunks and processed
    assert len(pipeline.df) == len(sample_df)

def test_run_pipeline(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.data_cleaning = MagicMock()  # Mock methods to avoid actual processing
    pipeline.data_transformation = MagicMock()
    pipeline.batch_process = MagicMock()
    pipeline.validate_and_store = MagicMock()

    pipeline.run_pipeline(n_chunks=2)

    # Check if all pipeline steps are called
    pipeline.data_cleaning.assert_called_once()
    pipeline.data_transformation.assert_called_once()
    pipeline.batch_process.assert_called_once_with(2)  # Corrected the argument here
    pipeline.validate_and_store.assert_called_once()
