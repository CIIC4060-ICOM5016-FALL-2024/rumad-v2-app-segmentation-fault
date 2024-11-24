from config.db_config import pg_config
import psycopg2 as pg


class SyllabusDAO:
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

    def insertSyllabus(self, courseid, embedding_text, chunk):
        cursor = self.conn.cursor()
        query = "INSERT INTO syllabus(courseid, embedding_text, chunk) VALUES(%s, %s, %s) RETURNING chunkid;"
        cursor.execute(query, (courseid, embedding_text, chunk))
        # chunkid = cursor.fetchone()[0]
        self.conn.commit()
        return courseid

    def getAllSyllabus(self):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, embedding_text as distance, chunk FROM syllabus order by distance limit 30;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllSyllabusByCid(self, courseid):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, embedding_text as distance , chunk FROM syllabus WHERE courseid = %s order by distance limit 30;"
        cursor.execute(query, [courseid])
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSyllabusById(self, chunkid):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, embedding_text as distance , chunk FROM syllabus WHERE chunkid = %s;"
        cursor.execute(query, [chunkid])
        result = cursor.fetchone()
        return result

    def getAllFragments(self, embedding_text):
        with self.conn.cursor() as cursor:
            query = """
            SELECT chunkid, courseid, chunk, embedding_text <=> %s as distance
            FROM syllabus 
            ORDER BY distance 
            LIMIT 30;
            """
            cursor.execute(query, (embedding_text,))
            result = cursor.fetchall()
        return result
