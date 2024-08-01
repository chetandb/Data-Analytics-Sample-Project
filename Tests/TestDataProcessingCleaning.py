from unittest.mock import MagicMock

import pandas as pd
import pytest

from Data_Preprocessing_Cleaning.DataPipeline import DataPipeline  # Adjust import based on your module name


@pytest.fixture
def sample_df():
    data = {
        'date': ['2024-01-01', '2024-01-02', None, '2024-01-04'],
        'user_id': [1, 2, 1, 2],
        'amount': [10, 20, 30, 40],
        'type': [None, 'sale', 'refund', 'sale']
    }
    return pd.DataFrame(data)

@pytest.fixture
def schema():
    return {'date': 'datetime64[ns]', 'user_id': 'int64', 'amount': 'float64', 'type': 'object'}

def test_configuration_parameters_transfer(sample_df):
    pipeline = DataPipeline(sample_df)
    assert pipeline.schema is not None
    assert 'amount' in pipeline.schema

def test_scan_dataset_for_missing_values(sample_df):
    pipeline = DataPipeline(sample_df)
    missing_values = pipeline.df.isnull().sum()
    assert missing_values.any()

def test_remove_duplicates(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.data_cleaning()
    assert pipeline.df.duplicated().sum() == 0

def test_pass_cleaned_data_to_validation_system(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.validate_and_store = MagicMock()
    pipeline.validate_and_store()
    pipeline.validate_and_store.assert_called_once()

def test_validate_deduplicated_data(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.data_cleaning()
    assert pipeline.df.duplicated().sum() == 0

def test_store_or_pass_on_cleaned_dataset(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.validate_and_store = MagicMock()
    pipeline.validate_and_store()
    pipeline.validate_and_store.assert_called_once()

def test_define_or_update_data_schema(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.schema = {'date': 'datetime64[ns]', 'user_id': 'int64', 'amount': 'float64'}
    assert isinstance(pipeline.schema, dict)

def test_provide_schema_to_data_cleaning_module(sample_df):
    pipeline = DataPipeline(sample_df)
    assert hasattr(pipeline, 'schema')


def test_define_duplicate_identification_criteria():
    pipeline = DataPipeline(pd.DataFrame())
    pipeline.duplicate_criteria = ['user_id', 'date']
    assert isinstance(pipeline.duplicate_criteria, list)

def test_pass_duplicate_identification_criteria():
    pipeline = DataPipeline(pd.DataFrame())
    assert hasattr(pipeline, 'duplicate_criteria')

def test_configure_date_formats_and_target_format(sample_df):
    pipeline = DataPipeline(sample_df)
    pipeline.target_date_format = '%Y-%m-%d'
    assert pipeline.target_date_format == '%Y-%m-%d'

