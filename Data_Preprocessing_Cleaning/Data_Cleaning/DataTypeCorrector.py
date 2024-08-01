import pandas as pd
import json

class DataTypeCorrector:
    def __init__(self, df, schema_file):
        self.df = df
        self.schema = self.load_schema(schema_file)

    def load_schema(self, schema_file):
        """
        Load the schema from a JSON file that defines the expected data types.

        :param schema_file: Path to the schema file
        :return: Dictionary with column names and their expected data types
        """
        with open(schema_file, 'r') as file:
            schema = json.load(file)
        return schema

    def correct_data_types(self):
        """
        Correct the data types in the dataset based on the schema.
        """
        for column, dtype in self.schema.items():
            if dtype == 'int':
                self.df[column] = self.df[column].astype('Int64')  # Using 'Int64' to handle NaNs in integers
            elif dtype == 'float':
                self.df[column] = self.df[column].astype('float64')
            elif dtype == 'date':
                self.df[column] = pd.to_datetime(self.df[column], errors='coerce')  # Converts invalid parsing to NaT
            else:
                raise ValueError(f"Unsupported data type: {dtype}")

        return self.df

# Example usage:
# df = pd.read_csv('data.csv')
# corrector = DataTypeCorrector(df, 'schema.json')
# corrected_df = corrector.correct_data_types()
