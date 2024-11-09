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

    def insertSection(self, roomid, cid, mid, semester, years, capacity):
        cursor = self.conn.cursor()
        query = "INSERT INTO section(roomid, cid, mid, semester, years, capacity) VALUES (%s, %s, %s, %s, %s, %s) RETURNING sid;"
        cursor.execute(query, (roomid, cid, mid, semester, years, capacity))
        sid = cursor.fetchone()
        self.conn.commit()
        return sid

    def deleteSectionBySid(self, sid):
        cursor = self.conn.cursor()
        query = "DELETE FROM section WHERE sid = %s;"
        cursor.execute(query, (sid,))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount > 0

    def updateSectionBySid(self, sid, roomid, cid, mid, semester, years, capacity):
        cursor = self.conn.cursor()
        query = "UPDATE section SET roomid = %s, cid = %s, mid = %s, semester = %s, years = %s, capacity = %s WHERE sid = %s RETURNING sid;"
        cursor.execute(query, (roomid, cid, mid, semester, years, capacity, sid))
        sid = cursor.fetchone()
        self.conn.commit()
        return sid

    def getSectionPerYear(self):
        cursor = self.conn.cursor()
        query = "SELECT years, count(sid) FROM section GROUP BY years ORDER BY years;"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    def getRatioByBuilding(self, building):
        result = []
        cursor = self.conn.cursor()
        query = """
            SELECT section.* FROM section 
            JOIN room on section.roomid = room.rid
            WHERE room.building = %s
            ORDER BY (section.capacity / room.capacity) DESC
            LIMIT 3;
        """
        cursor.execute(query, (building.capitalize(),))
        for row in cursor:
            result.append(row)
        return result
