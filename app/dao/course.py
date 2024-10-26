from config.db_config import pg_config
import psycopg2 as pg


class ClassDAO:
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

    def getAllClass(self):
            cursor = self.conn.cursor()
            query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class;"
            cursor.execute(query)
            result = []
            for row in cursor:
                result.append(row)
            return result
