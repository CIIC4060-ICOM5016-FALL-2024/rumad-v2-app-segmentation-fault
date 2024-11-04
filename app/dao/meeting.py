from config.db_config import pg_config
import psycopg2 as pg


class MeetingDAO:
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

    def getAllMeeting(self):
        cursor = self.conn.cursor()
        query = "SELECT mid, ccode, starttime, endtime, cdays FROM meeting;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMeetingByMid(self, mid):
        cursor = self.conn.cursor()
        query = (
            "SELECT mid, ccode, starttime, endtime, cdays FROM meeting WHERE mid = %s;"
        )
        cursor.execute(query, (mid,))
        result = cursor.fetchone()
        return result

    def insertMeeting(self, ccode, starttime, endtime, cdays):
        cursor = self.conn.cursor()
        query = "INSERT INTO meeting(ccode, starttime, endtime, cdays) VALUES (%s, %s, %s, %s) RETURNING mid;"
        cursor.execute(query, (ccode, starttime, endtime, cdays))
        mid = cursor.fetchone()
        self.conn.commit()
        return mid

    def updateMeetingByMid(self, mid, ccode, starttime, endtime, cdays):
        cursor = self.conn.cursor()
        query = "UPDATE meeting SET ccode = %s, starttime = %s, endtime = %s, cdays = %s WHERE mid = %s RETURNING mid;"
        cursor.execute(query, (ccode, starttime, endtime, cdays, mid))
        mid = cursor.fetchone()
        self.conn.commit()
        return mid

    def deleteMeetingByMid(self, mid):
        cursor = self.conn.cursor()
        query = "DELETE FROM meeting WHERE mid = %s;"
        cursor.execute(query, (mid,))
        rowcount = cursor.rowcount
        self.conn.commit()
        print(f"Deleted {rowcount} record(s) with mid={mid}")  # Add logging
        return rowcount > 0

    def getMostMeeting(self):
        cursor = self.conn.cursor()
        query = "SELECT m.mid, m.ccode, m.starttime, m.endtime, m.cdays, COUNT(s.sid) AS section_count FROM meeting m JOIN section s ON m.mid = s.mid GROUP BY m.mid, m.ccode, m.starttime, m.endtime, m.cdays ORDER BY section_count DESC LIMIT 5;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
