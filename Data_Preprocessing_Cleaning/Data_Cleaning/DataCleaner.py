import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df

    def handle_missing_values(self, strategy='mean', threshold=None, method=None):
        """
        Automatically handle missing values in the dataset.

        :param strategy: Strategy to handle missing values ('mean', 'median', 'mode', 'remove', 'ffill', 'bfill')
        :param threshold: Threshold for removing rows/columns with missing values
        :param method: Method for forward/backward filling ('ffill' or 'bfill')
        """
        if strategy == 'remove':
            if threshold:
                self.df.dropna(thresh=threshold, axis=0, inplace=True)
            else:
                self.df.dropna(inplace=True)
        elif strategy in ['mean', 'median', 'mode']:
            for column in self.df.select_dtypes(include=[np.number]).columns:
                if strategy == 'mean':
                    self.df[column] = self.df[column].fillna(self.df[column].mean())
                elif strategy == 'median':
                    self.df[column] = self.df[column].fillna(self.df[column].median())
                elif strategy == 'mode':
                    self.df[column].fillna(self.df[column].mode()[0], inplace=True)
        elif method in ['ffill', 'bfill']:
            self.df.fillna(method=method, inplace=True)
        else:
            raise ValueError(f"Unsupported strategy or method: {strategy}, {method}")

        return self.df

# Example usage:
# df = pd.read_csv('data.csv')
# cleaner = DataCleaner(df)
# cleaned_df = cleaner.handle_missing_values(strategy='median', threshold=10)
