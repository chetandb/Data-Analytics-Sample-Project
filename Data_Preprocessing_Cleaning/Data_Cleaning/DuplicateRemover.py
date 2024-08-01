import pandas as pd

class DuplicateRemover:
    def __init__(self, df):
        self.df = df

    def remove_duplicates(self, subset=None, keep='first'):
        """
        Remove duplicate records based on specified criteria.

        :param subset: Columns to consider for duplicate detection
        :param keep: Which duplicates to keep ('first', 'last', or False)
        """
        self.df.drop_duplicates(subset=subset, keep=keep, inplace=True)
        return self.df

# Example usage:
# df = pd.read_csv('data.csv')
# remover = DuplicateRemover(df)
# cleaned_df = remover.remove_duplicates(subset=['id'], keep='first')
