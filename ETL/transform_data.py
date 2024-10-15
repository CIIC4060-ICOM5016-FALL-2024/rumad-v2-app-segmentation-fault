from extract_data import run_etl


def main():
    # Call the run_etl function
    dataframes = run_etl()

    # Print each dataframe with its table name
    for i, (df, table_name) in enumerate(dataframes):
        print(f"DataFrame {i + 1} (Table: {table_name}):")
        print(df)
        print("\n" + "=" * 50 + "\n")  # Separator for clarity


if __name__ == "__main__":
    main()
