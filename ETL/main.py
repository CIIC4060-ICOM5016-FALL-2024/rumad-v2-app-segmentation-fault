from transform_data import clean_data
from DAO.insert_DAO import insert_to_db

def main():
    # Clean the data
    df_list = clean_data()
    
    for (df, table_name) in enumerate(df_list):
        insert_to_db(df, table_name)

    # Load the data into the database
    # This is where you would write the code to load the data into the database
    # print("Data loaded successfully")

if __name__ == "__main__":
    main()