from config.db_config import pg_config
import psycopg2 as pg


class FragmentsDAO:
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

    def insertFragment(self, did, content, embedding):
        cursor = self.conn.cursor()
        query = "INSERT INTO fragments(did, content, embedding) VALUES(%s, %s, %s) RETURNING fid;"
        cursor.execute(query, (did, content, embedding))
        fid = cursor.fetchone()[0]
        self.conn.commit()
        return fid
    
    
    def getAllFragments(self, emb):
        cursor = self.conn.cursor()
        query = "SELECT fid, did, content, embedding as distance FROM fragments where embedding = %s order my distance limit 30;"
        cursor.execute(query, (emb,))
        result = []
        for row in cursor:
            result.append(row)
        return result