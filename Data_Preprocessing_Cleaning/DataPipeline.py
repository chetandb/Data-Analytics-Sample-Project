import pandas as pd
import numpy as np
import logging
from concurrent.futures import ProcessPoolExecutor
import os
from typing import List, Dict

# Configure logging
logging.basicConfig(filename='data_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DataPipeline:
    def __init__(self, df: pd.DataFrame, schema: Dict[str, str] = None):
        self.df = df
        self.schema = schema if schema else self._infer_schema()
        self.duplicate_criteria = ['user_id', 'date']
        self.aggregation_rules = {'amount': 'sum'}
        self.target_date_format = '%Y-%m-%d'

    def _infer_schema(self) -> Dict[str, str]:
        """Infer data schema based on the dataframe's dtypes."""
        return {col: str(dtype) for col, dtype in self.df.dtypes.items()}

    def data_cleaning(self):
        try:
            logging.info('Data cleaning started.')
            self.df.fillna(method='ffill', inplace=True)  # Forward fill missing values
            for column, dtype in self.schema.items():
                if 'datetime' in dtype:
                    self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
                elif 'int' in dtype:
                    self.df[column] = pd.to_numeric(self.df[column], errors='coerce').astype('Int64')
                elif 'float' in dtype:
                    self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
            self.df.drop_duplicates(subset=self.duplicate_criteria, inplace=True)
            logging.info('Data cleaning completed.')
        except Exception as e:
            logging.error(f'Data cleaning failed: {e}')
            raise

    def data_transformation(self):
        try:
            logging.info('Data transformation started.')
            for column, rule in self.aggregation_rules.items():
                if column in self.df.columns:
                    self.df[f'{column}_aggregated'] = self.df.groupby('user_id')[column].transform(rule)
            logging.info('Data transformation completed.')
        except Exception as e:
            logging.error(f'Data transformation failed: {e}')
            raise

    def validate_and_store(self):
        try:
            logging.info('Validation and storage started.')
            assert not self.df.isnull().any().any(), 'Validation failed: Missing values present'
            for column, dtype in self.schema.items():
                assert str(self.df[column].dtype) == dtype, f'Validation failed: {column} has incorrect dtype'
            self.df.to_csv('cleaned_data.csv', index=False)
            logging.info('Validation and storage completed.')
        except AssertionError as e:
            logging.error(f'Validation failed: {e}')
            raise
        except Exception as e:
            logging.error(f'Storage failed: {e}')
            raise

    def batch_process(self, n_chunks: int):
        """
        Process data in batches to improve performance.

        :param n_chunks: Number of chunks to split the dataset into.
        """
        try:
            logging.info('Batch processing started.')
            chunks = np.array_split(self.df, n_chunks)
            with ProcessPoolExecutor() as executor:
                results = list(executor.map(self.process_chunk, chunks))
            self.df = pd.concat(results)
            logging.info('Batch processing completed.')
        except Exception as e:
            logging.error(f'Batch processing failed: {e}')
            raise

    def process_chunk(self, chunk: pd.DataFrame) -> pd.DataFrame:
        """
        Define your processing logic for each chunk here.

        :param chunk: A chunk of the dataset to process.
        :return: Processed chunk.
        """
        chunk.fillna(method='ffill', inplace=True)
        chunk.drop_duplicates(inplace=True)
        return chunk

    def run_pipeline(self, n_chunks: int = 4):
        """
        Run the entire data pipeline including cleaning, transformation, and validation.

        :param n_chunks: Number of chunks for batch processing.
        """
        try:
            logging.info('Pipeline execution started.')
            self.data_cleaning()
            self.data_transformation()
            self.batch_process(n_chunks)
            self.validate_and_store()
            logging.info('Pipeline execution completed.')
        except Exception as e:
            logging.error(f'Pipeline execution failed: {e}')
            raise

# Example usage
if __name__ == "__main__":
    print("Current Working Directory:", os.getcwd())
    try:
        df = pd.read_csv('path/to/your/raw_data.csv')  # Update this path
        pipeline = DataPipeline(df)
        pipeline.run_pipeline(n_chunks=4)
    except Exception as e:
        logging.error(f'Error in pipeline execution: {e}')
