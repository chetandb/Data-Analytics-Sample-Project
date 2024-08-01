import pandas as pd
import pytest
from DateParser import DateParser

@pytest.fixture
def sample_df():
    data = {
        'date_of_birth': ['1990-01-01', '02/28/1985', '31-12-2000', 'invalid_date'],
        'registration_date': ['01/01/2020', '2021-02-15', '15/03/2022', 'April 5, 2023']
    }
    return pd.DataFrame(data)

def test_parse_dates_invalid_format(sample_df):
    date_parser = DateParser(
        sample_df,
        date_columns=['date_of_birth', 'registration_date'],
        date_formats=['%Y/%m/%d']  # Using a format that doesn't match the data
    )
    parsed_df = date_parser.parse_dates()

    expected_data = {
        'date_of_birth': [pd.NaT, pd.NaT, pd.NaT, pd.NaT],
        'registration_date': [pd.NaT, pd.NaT, pd.NaT, pd.NaT]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(parsed_df, expected_df)
