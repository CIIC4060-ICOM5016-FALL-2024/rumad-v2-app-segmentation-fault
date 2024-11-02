import psycopg2
from DAO.db_config import pg_config


class DAO:
    def __init__(self):
        db_user = pg_config["user"]
        db_password = pg_config["password"]
        db_name = pg_config["dbname"]
        db_host = pg_config["host"]
        db_port = pg_config["port"]

        try:
            # Conection to the database
            self.conn = psycopg2.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_password,
                port=db_port,
            )
            # Create a cursor
            self.cursor = self.conn.cursor()
            print("Database connection established successfully.")

        except psycopg2.DatabaseError as error:
            print(f"Error connecting to the database: {error}")
            raise

    def initialize_schema(self):
        try:
            # Read the schema SQL file
            with open("schema.sql", "r") as file:
                sql_query = file.read()

            self.cursor.execute(sql_query)
            self.conn.commit()
            print("Database schema initialized successfully.")

        except Exception as e:
            print(f"Error executing schema SQL: {e}")
            self.conn.rollback()  # Rollback the transaction in case of an error

    def execute_sql_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                sql_query = file.read()
            self.cursor.execute(sql_query)
            self.conn.commit()
            print(f"Executed SQL file: {file_path}")
        except Exception as e:
            print(f"Error executing SQL file {file_path}: {e}")
            self.conn.rollback()  # Rollback the transaction in case of an error

    def close(self):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    dao = DAO()
    dao.initialize_schema()
    dao.close()
