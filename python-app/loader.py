import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
import logging
import json


# Configure logging
logging.basicConfig(filename='loader.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def _read_jsonl(file_path, file_schema):
    logging.info("Extracting data from source: %s", file_path)
    try:
        # Read the JSONL file into a pandas DataFrame
        df = pd.read_json(file_path, lines=True, dtype=file_schema)
        return df
    except Exception as e:
        logging.error("Error during data extraction: %s", str(e))
        raise


def _transform_df(df, table_columns):
    try:
        logging.info("Transforming data...")
        # Clean up of empty or 'null' string values to be null in the table
        df = df.replace(['', 'null'], np.nan)
        # Re-ordering columns to match the order of the table to then optimize the insert
        df = df[table_columns]
        return df
    except Exception as e:
        logging.error("Error during data transformation: %s", str(e))


def _load_data(df, database_url, table_name):
    try:
        # Create PostgresSQL connection
        engine = create_engine(database_url)
        logging.info("Loading data to table: %s", table_name)
        # Insert data into the crimes table in the database
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logging.info("Data successfully loaded.")
    except Exception as e:
        logging.error("Error during data loading: %s", str(e))
        raise


def process_and_insert_data():

    # Defining a config file
    TABLE_CONFIG_FILE = 'config.json'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    try:
        logging.info("ETL process started.")
        # Reading config file to get the parameters of the process
        with open(os.path.join(BASE_DIR, TABLE_CONFIG_FILE)) as config_file:
            logging.info("Loading Configurations...")
            CONFIG_FILE = json.load(config_file)

        # Defining variables to use during the process
        database_url = CONFIG_FILE['database_url']
        table_name = CONFIG_FILE['table_name']
        table_columns = CONFIG_FILE['table_columns']
        file_name = CONFIG_FILE['file_name']
        file_schema = CONFIG_FILE['file_schema']

        # Specify path/filename of source data file
        file_path = os.path.abspath(file_name)
        logging.info(f'file_path: {file_path}')
        # Function to get a Pandas Dataframe after reading jsonl source file
        raw_df = _read_jsonl(file_path, file_schema)
        # Function with the transformations logic returning the df to be inserted
        final_df = _transform_df(raw_df, table_columns)
        # Function to write the final df to the target table
        _load_data(final_df, database_url, table_name)
        logging.info("ETL process completed successfully.")
    except Exception as e:
        logging.error("ETL process failed: %s", str(e))

if __name__ == "__main__":
    process_and_insert_data()
