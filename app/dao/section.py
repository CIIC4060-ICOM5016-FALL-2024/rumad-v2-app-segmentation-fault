from config.db_config import pg_config
import psycopg2 as pg


class SectionDAO:
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

    def getAllSection(self):
        cursor = self.conn.cursor()
        query = "SELECT sid, roomid, cid, mid, semester, years, capacity FROM section;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSectionBySid(self, sid):
        cursor = self.conn.cursor()
        query = "SELECT sid, roomid, cid, mid, semester, years, capacity FROM section WHERE sid = %s;"
        cursor.execute(query, (sid,))
        result = cursor.fetchone()
        return result
