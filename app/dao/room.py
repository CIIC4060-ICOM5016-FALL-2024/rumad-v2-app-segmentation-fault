from config.db_config import pg_config
import psycopg2 as pg

class RoomDAO:
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

    def getAllRoom(self):
        result = []
        cursor = self.conn.cursor()
        query = "SELECT rid, building, room_number, capacity FROM room;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result
