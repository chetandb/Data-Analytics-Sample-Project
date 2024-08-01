import pytest
import pandas as pd
from io import StringIO
import json
import os

from Data_Preprocessing_Cleaning.Data_Cleaning.DataTypeCorrector import DataTypeCorrector

# Sample schema and data for testing
schema_json = {
    "A": "int",
    "B": "float",
    "C": "date"
}

sample_data = """
A,B,C
1,2.5,2023-01-01
2,,2023-02-01
,4.5,invalid_date
4,5.5,2023-04-01
"""

@pytest.fixture
def sample_df():
    return pd.read_csv(StringIO(sample_data))

@pytest.fixture
def schema_file(tmpdir):
    file_path = os.path.join(tmpdir, "schema.json")
    with open(file_path, "w") as f:
        json.dump(schema_json, f)
    return file_path

def test_load_schema(schema_file):
    corrector = DataTypeCorrector(pd.DataFrame(), schema_file)
    schema = corrector.load_schema(schema_file)
    assert schema == schema_json

def test_correct_data_types(sample_df, schema_file):
    corrector = DataTypeCorrector(sample_df, schema_file)
    corrected_df = corrector.correct_data_types()

    assert corrected_df['A'].dtype == 'Int64'
    assert corrected_df['B'].dtype == 'float64'
    assert corrected_df['C'].dtype == 'datetime64[ns]'

    # Check if NaNs are handled correctly in 'A'
    assert corrected_df['A'].isna().sum() == 1

    # Check if invalid dates are converted to NaT
    assert pd.isna(corrected_df.loc[2, 'C'])

def test_unsupported_data_type(sample_df, tmpdir):
    invalid_schema_json = {
        "A": "int",
        "B": "unsupported_type"
    }
    file_path = os.path.join(tmpdir, "invalid_schema.json")
    with open(file_path, "w") as f:
        json.dump(invalid_schema_json, f)

    with pytest.raises(ValueError, match="Unsupported data type: unsupported_type"):
        corrector = DataTypeCorrector(sample_df, file_path)
        corrector.correct_data_types()

# To run the tests, use the following command in the terminal:
# pytest -v
