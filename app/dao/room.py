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

    def getRoomByRid(self, rid):
        cursor = self.conn.cursor()
        query = "SELECT * FROM room WHERE rid=%s"
        cursor.execute(query, (rid,))
        return cursor.fetchone()

    def insertRoom(self, building, room_number, capacity):
        cursor = self.conn.cursor()

        conflict_check_query = (
            "SELECT 1 FROM room WHERE building = %s AND room_number = %s"
        )
        cursor.execute(conflict_check_query, (building, room_number))
        if cursor.fetchone():
            return None

        query = "INSERT INTO room (building, room_number, capacity) VALUES (%s, %s, %s) RETURNING rid;"
        cursor.execute(query, (building, room_number, capacity))
        result = cursor.fetchone()
        self.conn.commit()
        if result:
            return result[0]
        else:
            return None

    def deleteRoomByRid(self, rid):
        cursor = self.conn.cursor()
        query = "DELETE FROM room WHERE rid=%s"
        cursor.execute(query, (rid,))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1

    def updateRoomByRid(self, rid, building, room_number, capacity):
        cursor = self.conn.cursor()

        conflict_check_query = (
            "SELECT 1 FROM room WHERE building = %s AND room_number = %s AND rid != %s"
        )
        cursor.execute(conflict_check_query, (building, room_number, rid))
        if cursor.fetchone():
            return False

        query = "UPDATE room SET building=%s, room_number=%s, capacity=%s WHERE rid=%s"
        cursor.execute(query, (building, room_number, capacity, rid))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1

    def getMaxCapacity(self, building):
        result = []
        cursor = self.conn.cursor()
        query = "SELECT * FROM room WHERE building=%s ORDER BY capacity DESC LIMIT 3;"
        cursor.execute(query, (building.capitalize(),))
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
        cursor.execute(query, (building.capitalize(),))
        for row in cursor:
            result.append(row)
        return result
