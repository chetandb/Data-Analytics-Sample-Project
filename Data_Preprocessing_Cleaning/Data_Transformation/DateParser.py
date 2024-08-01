import pandas as pd
import re

class DateParser:
    def __init__(self, df, date_columns, date_formats=None):
        self.df = df
        self.date_columns = date_columns
        self.date_formats = date_formats

    def parse_dates(self):
        """
        Convert date and time information from raw formats into standardized formats.
        """
        for column in self.date_columns:
            if self.date_formats:
                for date_format in self.date_formats:
                    try:
                        self.df[column] = pd.to_datetime(self.df[column], format=date_format, errors='coerce')
                        break  # Exit loop once successful
                    except ValueError:
                        continue
            else:
                self.df[column] = pd.to_datetime(self.df[column], errors='coerce')

        return self.df

# Example usage:
# df = pd.read_csv('data.csv')
# date_parser = DateParser(df, date_columns=['date_of_birth', 'registration_date'], date_formats=['%Y-%m-%d', '%m/%d/%Y'])
# df = date_parser.parse_dates()
