import psycopg2
from DAO.db_config import pg_config

class DAO:
    def __init__(self):
        db_user = pg_config['user']
        db_password = pg_config['password']
        db_name = pg_config['dbname']
        db_host = pg_config['host']
        db_port = pg_config['port']
        
        try:
            # Conexión a la base de datos usando psycopg2
            self.conn = psycopg2.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_password,
                port=db_port
            )
            self.cursor = self.conn.cursor()  # Crear un cursor para ejecutar consultas
            print("Database connection established successfully.")
        
        except psycopg2.DatabaseError as error:
            print(f"Error connecting to the database: {error}")
            raise
    
    def initialize_schema(self):
        try:
            # Leer y ejecutar el schema.sql
            with open("schema.sql", "r") as file:
                sql_query = file.read()

            self.cursor.execute(sql_query)
            self.conn.commit()
            print("Database schema initialized successfully.")
        
        except Exception as e:
            print(f"Error executing schema SQL: {e}")
            self.conn.rollback()  # Hacer rollback en caso de error

    def close(self):
        # Cerrar el cursor y la conexión
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    dao = DAO()
    dao.initialize_schema()
    dao.close()
