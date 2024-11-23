from config.db_config import pg_config
import psycopg2 as pg

class RegistrationDAO():
  def __init__(self):
        # Create the connection string
        url = "dbname=%s password=%s user=%s host=%s port=%s" % (
            pg_config["dbname"],
            pg_config["password"],
            pg_config["user"],
            pg_config["host"],
            pg_config["port"],
        )

        self.conn = pg.connect(url)
      
  def logInUser(self, username, password):
        cursor = self.conn.cursor()
        query = 'SELECT * FROM "user" WHERE "username" = %s AND "password" = %s;'
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return result
      
  def signUpUser(self, username, password):
          cursor = self.conn.cursor()
          try:
              query = 'INSERT INTO "user" ("username", "password") VALUES (%s, %s) RETURNING "username";'
              cursor.execute(query, (username, password))
              username = cursor.fetchone()[0]  # type: ignore
              self.conn.commit()
              return username
          except pg.IntegrityError:
              # Capturamos errores de integridad, como el duplicado del username
              self.conn.rollback()  # Revertimos la transacción en caso de error
              raise ValueError("Username already exists.")
          finally:
              cursor.close()