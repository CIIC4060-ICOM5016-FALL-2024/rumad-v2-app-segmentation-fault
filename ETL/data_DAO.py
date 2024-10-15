from sqlalchemy import create_engine
import psycopg2
import pandas as pd
from extract_data import run_etl


class DAO:
    def __init__(self):
        db_user = "ubj1eoeaku13t6"
        db_password = (
            "pdef0051a9c37a2f131b786f09aaeb192dffcbe140fe7d048dcc6c62342c3dbcc"
        )
        db_name = "d4i4fjj12gdddt"
        db_host = "c3cj4hehegopde.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
        db_port = 5432
        self.conn2 = create_engine(
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        self.conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port,
        )
        with open("schema.sql", "r") as file:
            sql_query = file.read()
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        self.conn.commit()

    def write_database(self, df, table_name, connection, if_table_exists="append"):
        cursor = self.conn.cursor()

        for index, row in df.iterrows():
            columns = ", ".join(row.index)
            values = ", ".join([f"'{str(value)}'" for value in row.values])
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            cursor.execute(insert_query)

        self.conn.commit()
        cursor.close()
        print(
            f"Inserted DataFrame into table {table_name} with if_exists={if_table_exists}"
        )

    def insert_dataframes(self, dataframes):
        # Define the order of tables based on foreign key dependencies
        table_order = ["class", "room", "meeting", "section", "requisite"]

        # Create a dictionary to map table names to dataframes
        table_to_df = {table_name: df for df, table_name in dataframes}

        # Insert data into tables in the correct order
        for table_name in table_order:
            if table_name in table_to_df:
                self.write_database(
                    df=table_to_df[table_name],
                    table_name=table_name,
                    connection=self.conn2,
                    if_table_exists="append",
                )


if __name__ == "__main__":
    dao = DAO()
    dataframes = run_etl()
    dao.insert_dataframes(dataframes)
