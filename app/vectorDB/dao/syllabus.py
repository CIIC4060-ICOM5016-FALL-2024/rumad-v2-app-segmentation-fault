from config.db_config import pg_config
import psycopg2 as pg

class SyllabusDao:
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

    def insertSyllabus(self, cid, embedding_text, chunk):
        cursor = self.conn.cursor()
        query = "INSERT INTO syllabus(courseid, embedding_text, chunk) VALUES(%s, %s, %s) RETURNING chunkid;"
        cursor.execute(query, (cid, embedding_text, chunk))
        sid = cursor.fetchone()[0]
        self.conn.commit()
        return cid
    
    def getAllSyllabus(self):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, embedding_text, chunk as distance FROM syllabus order my distance limit 30;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getAllSyllabusByCid(self, cid):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, embedding_text, chunk as distance FROM syllabus WHERE couserid = %s;"
        cursor.execute(query, [cid])
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getSyllabusById(self, sid):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, embedding_text, chunk as distance FROM syllabus WHERE chunkid = %s;"
        cursor.execute(query, [sid])
        result = cursor.fetchone()
        return result