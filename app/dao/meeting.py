from config.db_config import pg_config
from datetime import datetime

import psycopg2 as pg

def convert_to_minutes(time_str):
    hours, minutes, _ = map(int, time_str.split(':'))
    return hours * 60 + minutes

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

    def checkMeetingDuplication(self, ccode, starttime, endtime, cdays):
        cursor = self.conn.cursor()
        conflict_check_query = "SELECT 1 FROM meeting WHERE ccode = %s AND starttime = %s AND endtime = %s AND cdays = %s;"
        cursor.execute(conflict_check_query, (ccode, starttime, endtime, cdays))
        if cursor.fetchone():
            return None
        return 1

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

        if not self.checkMeetingDuplication(ccode, starttime, endtime, cdays):
            return None
        
        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")

        query = "INSERT INTO meeting(ccode, starttime, endtime, cdays) VALUES (%s, %s, %s, %s) RETURNING mid;"
        cursor.execute(query, (ccode, starttime_dt, endtime_dt, cdays))
        mid = cursor.fetchone()
        self.conn.commit()
        return mid
    
    def insertMeetingAndDisplaceByTimeAmout(self, ccode, starttime, endtime, cdays, delta_time_to_left, delta_time_to_right):
        cursor = self.conn.cursor()

        if not self.checkMeetingDuplication(ccode, starttime, endtime, cdays):
            return None
        
        str_left = delta_time_to_left
        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")
        delta_time_to_right = datetime.strptime(delta_time_to_right.split(":")[0] + ":" + delta_time_to_right.split(":")[1], "%H:%M")
        delta_time_to_left = datetime.strptime(delta_time_to_left.split(":")[0] + ":" + delta_time_to_left.split(":")[1], "%H:%M")
    
        insert_meeting_query = """
                INSERT INTO meeting(ccode, starttime, endtime, cdays)
                VALUES (%s, %s + %s::interval, %s + %s::interval, %s) RETURNING mid;
            """
        
        if str_left == "00:00":
            cursor.execute(insert_meeting_query, (ccode, starttime_dt.time(), delta_time_to_right.time(), endtime_dt.time(), delta_time_to_right.time(), cdays))
            print("inserting to the right")
        else:
            cursor.execute(insert_meeting_query, (ccode, starttime_dt.time(), delta_time_to_left.time(), endtime_dt.time(), delta_time_to_left.time(), cdays))
            print("inserting to the left")
            
        mid = cursor.fetchone()

        if mid:
            adjust_meeting_query = """
                UPDATE meeting SET starttime = starttime + %s::interval, endtime = endtime + %s::interval
                WHERE cdays = %s AND ((starttime >= %s) OR (endtime > %s));
            """
            cursor.execute(adjust_meeting_query, (delta_time_to_right.time(), delta_time_to_right.time(), cdays, starttime_dt.time(), endtime_dt.time()))
            adjust_meeting_query = """
                UPDATE meeting SET starttime = starttime - %s::interval, endtime = endtime - %s::interval
                WHERE cdays = %s AND ((starttime < %s) OR (endtime <= %s));
            """
            cursor.execute(adjust_meeting_query, (delta_time_to_left.time(), delta_time_to_left.time(), cdays, starttime_dt.time(), endtime_dt.time()))

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
