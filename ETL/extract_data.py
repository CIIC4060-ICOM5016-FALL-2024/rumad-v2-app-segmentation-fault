import os
import pandas as pd
import sqlite3
import json

# Paths for raw data (input) and processed data (output)
RAW_DATA_FOLDER = "./../data"


# Function to extract data from SQLite database
def extract_db(file_path):
    conn = sqlite3.connect(file_path)
    table_name = "requisites"
    df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df


def run_etl():
    dataframes = []  # List to store all dataframes

    # Iterate over all files in the raw_data folder
    for file_name in os.listdir(RAW_DATA_FOLDER):
        file_path = os.path.join(RAW_DATA_FOLDER, file_name)

        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
            if df is not None:
                processed_data = df.dropna()
                dataframes.append(processed_data)

        elif file_name.endswith(".db"):
            df = extract_db(file_path)
            if df is not None:
                processed_data = df.dropna()
                dataframes.append(processed_data)

        elif file_name.expandtabs(".json"):
            df = json.load(file_path)
            if df is not None:
                processed_data = pd.DataFrame([(key, item['number'], item['capacity']) for key, values in df.items() for item in values],
                                columns=['Building', 'Number', 'Capacity'])
                dataframes.append(processed_data)
            
            

    return dataframes


if __name__ == "__main__":
    run_etl()
