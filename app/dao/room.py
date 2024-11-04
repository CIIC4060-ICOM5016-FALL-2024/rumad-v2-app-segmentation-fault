from config.db_config import pg_config
import psycopg2 as pg

class RoomDAO:
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

    def getAllRoom(self):
        result = []
        cursor = self.conn.cursor()
        query = "SELECT * FROM room;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def  getRoomByRid(self, rid):
        cursor = self.conn.cursor()
        query = "SELECT * FROM room WHERE rid=%s"
        cursor.execute(query, (rid,))
        return cursor.fetchone()

    def insertRoom(self, building, room_number, capacity):
        cursor = self.conn.cursor()
        query = "INSERT INTO room (building, room_number, capacity) VALUES (%s, %s, %s) RETURNING rid;"
        cursor.execute(query, (building, room_number, capacity))
        rid = cursor.fetchone()[0]
        self.conn.commit()
        return rid

    def deleteRoomByRid(self, rid):
        cursor = self.conn.cursor()
        query = "DELETE FROM room WHERE rid=%s"
        cursor.execute(query, (rid,))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1

    def updateRoomByRid(self, rid, building, room_number, capacity):
        cursor = self.conn.cursor()
        query = "UPDATE room SET building=%s, room_number=%s, capacity=%s WHERE rid=%s"
        cursor.execute(query, (building, room_number, capacity, rid))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1

    def getMaxCapacity(self, building):
        result = []
        cursor = self.conn.cursor()
        query = "SELECT * FROM room WHERE building=%s ORDER BY capacity DESC LIMIT 3;"
        cursor.execute(query, (building,))
        for row in cursor:
            result.append(row)
        return result
    
    def getRatioByBuilding(self, building):
        result = []
        cursor = self.conn.cursor()
        query = """
            SELECT room.*
            FROM room
            JOIN section ON room.rid = section.roomid
            WHERE room.building = %s
            ORDER BY (section.capacity / room.capacity) DESC
            LIMIT 3;
        """
        cursor.execute(query, (building,))
        for row in cursor:
            result.append(row)
        return result
    
    def getMostClassesByRid(self, rid):
        result = []
        cursor = self.conn.cursor()
        query = """
            SELECT class.* 
            FROM class
            JOIN section ON class.cid = section.cid
            JOIN room ON room.rid = section.roomid
            WHERE room.rid = %s
            GROUP BY class.cid
            ORDER BY COUNT(section.cid) DESC
            LIMIT 3;
        """        
        cursor.execute(query, (rid,))
        for row in cursor:
            result.append(row)
        return result


