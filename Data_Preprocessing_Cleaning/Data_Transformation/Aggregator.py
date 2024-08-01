import pandas as pd

class Aggregator:
    def __init__(self, df):
        self.df = df

    def calculate_aggregated_values(self, group_by_columns, calculations):
        """
        Generate new fields by aggregating or calculating data from existing columns.

        :param group_by_columns: List of columns to group by.
        :param calculations: Dictionary with column names and aggregation functions.
        """
        aggregated_df = self.df.groupby(group_by_columns).agg(calculations).reset_index()
        return aggregated_df

# Example usage:
# df = pd.read_csv('data.csv')
# aggregator = Aggregator(df)
# calculations = {
#     'amount': 'sum',
#     'age': 'mean'
# }
# aggregated_df = aggregator.calculate_aggregated_values(['user_id'], calculations)
