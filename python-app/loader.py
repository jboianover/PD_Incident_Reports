import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2 import Geometry
import os
import logging
import json
from geopandas import gpd
from shapely.geometry import Point
import datetime


# Get the current timestamp as a string
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
log_file_name = f'loader_{timestamp}.log'

# Configure logging
logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# Defining a config file
TABLE_CONFIG_FILE = 'config.json'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
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
view_sql = CONFIG_FILE['view_sql']

# Build the absolute file path
view_sql_path = os.path.join(BASE_DIR, "..", view_sql)


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
        df.replace(['', 'null'], np.nan, inplace=True)
        df['filed_online'].fillna('false', inplace=True)
        # Create a mask to filter out rows where both latitude and longitude are not null
        mask = (df['latitude'].notna()) & (df['longitude'].notna())
        # Create a GeoDataFrame with the 'geometry' column
        geometry = [Point(lon, lat) if m and lon and lat else None for lon, lat, m in
                    zip(df['longitude'], df['latitude'], mask)]
        df = df.drop(['point'], axis=1)
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
        # Rename the 'geometry' column to 'point'
        gdf = gdf.rename(columns={'geometry': 'point'})
        df = pd.concat([df, gdf['point']], axis=1)
        df['point'] = df['point'].apply(lambda geom: geom.wkt if geom else None)
        # Re-ordering columns to match the order of the table to then optimize the insert
        df = df[table_columns]
        return df
    except Exception as e:
        logging.error("Error during data transformation: %s", str(e))
        raise


def _load_data(df, database_url, table_name):
    try:
        # Create PostgresSQL connection
        engine = create_engine(database_url)
        logging.info("Loading data to table: %s", table_name)
        # Insert data into the crimes table in the database
        df.to_sql(table_name, engine, if_exists='append', index=False,
                  dtype={'point': Geometry('POINT', srid=4326)})
        logging.info("Data successfully loaded.")
    except Exception as e:
        logging.error("Error during data loading: %s", str(e))
        raise


def _run_post_load_commands(database_url, table_name):
    engine = create_engine(database_url)
    analyze_sql = f"ANALYZE {table_name};"
    with open(view_sql_path, 'r') as sql_file:
        view_sql = sql_file.read()
    sql_commands = [analyze_sql, view_sql]
    try:
        with engine.connect() as connection:
            for command in sql_commands:
                connection.execute(command)
    except SQLAlchemyError as e:
        print(f"Error executing SQL command: {e}")
        raise


def process_and_insert_data():
    try:
        logging.info("ETL process started.")
        # Specify path/filename of source data file
        file_path = os.path.abspath(file_name)
        logging.info(f'file_path: {file_path}')
        # Function to get a Pandas Dataframe after reading jsonl source file
        raw_df = _read_jsonl(file_path, file_schema)
        # Function with the transformations logic returning the df to be inserted
        final_df = _transform_df(raw_df, table_columns)
        # Function to write the final df to the target table
        _load_data(final_df, database_url, table_name)
        logging.info("Now runnning post-load routines")
        _run_post_load_commands(database_url, table_name)
        logging.info("ETL process completed successfully.")
    except Exception as e:
        logging.error("ETL process failed: %s", str(e))


if __name__ == "__main__":
    process_and_insert_data()
