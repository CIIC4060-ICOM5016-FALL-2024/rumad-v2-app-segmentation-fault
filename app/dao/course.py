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
        cid = cursor.fetchone()[0] #type: ignore
        self.conn.commit()
        return cid
    
    def updateClassById(self, cid, cname, ccode, cdesc, term, years, cred, csyllabus):
        #TODO Verify if class with cid exists if not return a message
        cursor = self.conn.cursor()
        query = "UPDATE class SET cname = %s, ccode = %s, cdesc = %s, term = %s, years = %s, cred = %s, csyllabus = %s WHERE cid = %s;"
        cursor.execute(query, [cname, ccode, cdesc, term, years, cred, csyllabus, cid])
        self.conn.commit()
        #return boolean if the update was successful
        rowcount = cursor.rowcount
        return rowcount == 1
    
    def deleteClassById(self, cid):
        #TODO Verify if class with cid exists if not return a message
        cursor = self.conn.cursor()
        query = "DELETE FROM class WHERE cid = %s;"
        cursor.execute(query, [cid])
        self.conn.commit()
        rowcount = cursor.rowcount
        return rowcount == 1
    
    def getMostPrerequisite(self):
        cursor = self.conn.cursor()
        query = "SELECT c.cid, c.cname, c.ccode, c.cdesc, c.term, c.years, c.cred, c.csyllabus, COUNT(r.classid) AS most_prerequisite_class FROM requisite AS r INNER JOIN class AS c ON r.reqid = c.cid WHERE r.prereq = TRUE AND cid != 37 GROUP BY c.cid, c.cname, c.ccode, c.cdesc, c.term, c.years, c.cred, c.csyllabus ORDER BY most_prerequisite_class DESC LIMIT 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

         
