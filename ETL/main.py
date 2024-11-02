from transform_data import clean_data
from DAO.insert_DAO import insert_to_db
from DAO.data_DAO import DAO


def main():
    # Initialize the schema
    dao = DAO()
    dao.initialize_schema()
    dao.close()

    # Clean the data
    df_list = clean_data()

    #  Insert the data into the database
    for df, table_name in df_list:
        insert_to_db(df, table_name)

    # Reopen the connection to execute the SQL files
    dao = DAO()
    dao.execute_sql_file("sequences.sql")
    dao.close()


if __name__ == "__main__":
    main()
