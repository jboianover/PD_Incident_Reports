import os
import pandas as pd
import psycopg2


def _read_jsonl(file):
    # Read the JSONL file into a pandas DataFrame
    df = pd.read_json(file, lines=True)

    return df


def _transform_df(df):
    pass


def _load_data(df, database_url):
    try:
        conn = psycopg2.connect(database_url)
        # Insert data into the database
        df.to_sql('your_table_name', conn, if_exists='replace', index=False)

    except Exception as e:
        print(f"Error: {e}")

    return


def process_and_insert_data():
    # Read the DATABASE_URL environment variable
    database_url = os.environ.get("DATABASE_URL")

    # Specify path/filename of source data file
    file_path = 'sf_crime_reports.jsonl'
    df = _read_jsonl(file_path)
    final_df = _transform_df(df)
    _load_data(final_df, database_url)


if __name__ == "__main__":
    process_and_insert_data()
