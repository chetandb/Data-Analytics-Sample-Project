import pytest
import pandas as pd
from DuplicateRemover import DuplicateRemover

@pytest.fixture
def sample_df():
    data = {
        'id': [1, 2, 2, 3, 4, 4, 5],
        'value': ['A', 'B', 'B', 'C', 'D', 'D', 'E']
    }
    return pd.DataFrame(data)

def test_remove_duplicates_keep_first(sample_df):
    remover = DuplicateRemover(sample_df.copy())
    cleaned_df = remover.remove_duplicates(subset=['id'], keep='first')

    # Ensure duplicates are removed and only first occurrence is kept
    assert cleaned_df.shape[0] == 5
    assert cleaned_df['id'].tolist() == [1, 2, 3, 4, 5]

def test_remove_duplicates_keep_last(sample_df):
    remover = DuplicateRemover(sample_df.copy())
    cleaned_df = remover.remove_duplicates(subset=['id'], keep='last')

    # Ensure duplicates are removed and only last occurrence is kept
    assert cleaned_df.shape[0] == 5
    assert cleaned_df['id'].tolist() == [1, 2, 3, 4, 5]

def test_remove_duplicates_keep_false(sample_df):
    remover = DuplicateRemover(sample_df.copy())
    cleaned_df = remover.remove_duplicates(subset=['id'], keep=False)

    # Ensure all duplicates are removed
    assert cleaned_df.shape[0] == 3
    assert cleaned_df['id'].tolist() == [1, 3, 5]

def test_remove_duplicates_no_subset(sample_df):
    remover = DuplicateRemover(sample_df.copy())
    cleaned_df = remover.remove_duplicates(keep='first')

    # Ensure duplicates are removed based on all columns
    assert cleaned_df.shape[0] == 5

if __name__ == '__main__':
    pytest.main()
