import os
import pandas as pd
import sqlite3

# Paths for raw data (input) and processed data (output)
RAW_DATA_FOLDER = "data/raw"

# Ensure the output directory exists
os.makedirs("data/extracted", exist_ok=True)


# Function to extract data from CSV files
def extract_csv(file_path):
    df = pd.read_csv(file_path)
    return df


# Function to extract data from SQLite database
def extract_db(file_path):
    conn = sqlite3.connect(file_path)
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    dfs = {}
    for table_name in tables["name"]:
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
        dfs[table_name] = df
    conn.close()
    return dfs


# Function to transform the data (e.g., removing rows with missing values)
def transform_data(df):
    df_cleaned = df.dropna()
    return df_cleaned


def run_etl():
    # Iterate over all files in the raw_data folder
    for file_name in os.listdir(RAW_DATA_FOLDER):
        file_path = os.path.join(RAW_DATA_FOLDER, file_name)

        if file_name.endswith(".csv"):
            df = extract_csv(file_path)
            if df is not None:
                processed_data = transform_data(df)
                output_filename = f"extracted_{file_name.replace('.csv', '.csv')}"
                processed_data.to_csv(f"data/extracted/{output_filename}", index=False)

        elif file_name.endswith(".db"):
            dfs = extract_db(file_path)
            if dfs is not None:
                for table_name, df in dfs.items():
                    processed_data = transform_data(df)
                    output_filename = f"extracted_{file_name.replace('.db', '')}.csv"
                    processed_data.to_csv(
                        f"data/extracted/{output_filename}", index=False
                    )


if __name__ == "__main__":
    run_etl()
