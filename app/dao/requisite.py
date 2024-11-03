from config.db_config import pg_config
import psycopg2 as pg


class RequisiteDAO:
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

    def getAllRequisite(self):
        cursor = self.conn.cursor()
        query = "SELECT classid, reqid, prereq FROM requisite;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRequisiteByClassIdReqId(self, classid, reqid):
        cursor = self.conn.cursor()
        query = "SELECT classid, reqid, prereq FROM requisite WHERE classid = %s AND reqid = %s;"
        cursor.execute(query, (classid, reqid))
        result = cursor.fetchone()
        return result
    
    def insertRequisite(self, classid, reqid, prereq):
        cursor = self.conn.cursor()
        query = "INSERT INTO requisite(classid, reqid, prereq) VALUES (%s, %s, %s) RETURNING classid, reqid;"
        cursor.execute(query, (classid, reqid, prereq))
        ids = cursor.fetchone()
        self.conn.commit()
        return ids

    def deleteRequisiteByClassIdReqId(self, classid, reqid):
        cursor = self.conn.cursor()
        query = "DELETE FROM requisite WHERE classid = %s AND reqid = %s;"
        cursor.execute(query, (classid, reqid))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount > 0
    
