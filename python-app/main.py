import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os


def _read_jsonl(file_path):

    schema = {
        "incident_datetime": "datetime64[ns]",
        "incident_date": "datetime64[ns]",
        "incident_time": "object",
        "incident_year": "int64",
        "incident_day_of_week": "object",
        "report_datetime": "datetime64[ns]",
        "row_id": "int64",
        "incident_id": "int64",
        "incident_number": "int64",
        "cad_number": "object",
        "report_type_code": "object",
        "report_type_description": "object",
        "filed_online": "object",
        "incident_code": "object",
        "incident_category": "object",
        "incident_subcategory": "object",
        "incident_description": "object",
        "resolution": "object",
        "intersection": "object",
        "cnn": "object",
        "police_district": "object",
        "analysis_neighborhood": "object",
        "supervisor_district": "int64",
        "latitude": "float64",
        "longitude": "float64",
        "point": "object"
    }

    # Read the JSONL file into a pandas DataFrame
    df = pd.read_json(file_path, lines=True, dtype=schema)

    return df


def _transform_df(df):
    # Clean up of empty or 'null' string values to be null in the table
    df = df.replace(['', 'null'], np.nan)
    # Re-ordering columns to match the order of the table to then optimize the insert
    df = df[['row_id', 'incident_id', 'incident_number', 'cad_number', 'incident_datetime',
             'incident_date', 'incident_time', 'incident_year', 'incident_day_of_week',
             'report_datetime', 'report_type_code', 'report_type_description', 'filed_online',
             'incident_code', 'incident_category', 'incident_subcategory', 'incident_description',
             'resolution', 'intersection', 'cnn', 'police_district', 'analysis_neighborhood',
             'supervisor_district', 'latitude', 'longitude', 'point']]
    return df


def _load_data(df, database_url):
    try:
        # Create PostgresSQL connection
        engine = create_engine(database_url)
        # Insert data into the crimes table in the database
        df.to_sql('crimes', engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Error: {e}")

    return


def process_and_insert_data():
    # Read the DATABASE_URL environment variable
    database_url = 'postgresql://admin:admin@localhost:5433/PD_Incidents'
    print(database_url)

    # Specify path/filename of source data file
    file_path = os.path.abspath('sf_crime_reports.jsonl')
    print(f'file_path: {file_path}')
    df = _read_jsonl(file_path)
    final_df = _transform_df(df)
    _load_data(final_df, database_url)


if __name__ == "__main__":
    process_and_insert_data()
