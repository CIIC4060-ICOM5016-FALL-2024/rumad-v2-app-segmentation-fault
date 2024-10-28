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
    
    def getClassById(self, cid):
        cursor = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class WHERE cid = %s;"
        cursor.execute(query, [cid])
        result = cursor.fetchone()
        return result
    
    def insertClass(self, cname, ccode, cdesc, term, years, cred, csyllabus):
        cursor = self.conn.cursor()
        query = "INSERT INTO class(cname, ccode, cdesc, term, years, cred, csyllabus) VALUES (%s, %s, %s, %s, %s, %s, %s) returning cid;"
        cursor.execute(query, [cname, ccode, cdesc, term, years, cred, csyllabus])
        cid = cursor.fetchone()[0]
        self.conn.commit()
        return cid
    
    def updateClass(self, cid, cname, ccode, cdesc, term, years, cred, csyllabus):
        cursor = self.conn.cursor()
        query = "UPDATE class SET cname = %s, ccode = %s, cdesc = %s, term = %s, years = %s, cred = %s, csyllabus = %s WHERE cid = %s;"
        cursor.execute(query, [cname, ccode, cdesc, term, years, cred, csyllabus, cid])
        self.conn.commit()
        return cid

         
