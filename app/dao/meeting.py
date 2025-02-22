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

    def checkMeetingDuplicate(self, ccode, starttime, endtime, cdays):
        # print(ccode, starttime, endtime, cdays)
        cursor = self.conn.cursor()
        conflict_check_query = "SELECT mid FROM meeting WHERE ccode = %s AND starttime = %s::time AND endtime = %s::time AND cdays = %s;"
        cursor.execute(conflict_check_query, (ccode, starttime, endtime, cdays))
        mid = cursor.fetchone()
        return mid
    
    def checkMeetingConflict(self, starttime, endtime, cdays):
        cursor = self.conn.cursor()
        conflict_query = """
            SELECT * 
            FROM meeting 
            WHERE cdays = %s AND 
            ((starttime < %s AND endtime >= %s) 
            OR (starttime <= %s AND endtime > %s));
        """
        cursor.execute(conflict_query, (cdays, starttime, starttime, endtime, endtime))
        result = []
        for row in cursor:
            result.append(row)
        return result


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

    def insertMeeting(self, ccode, starttime, endtime, cdays, delta_time_to_left=None, delta_time_to_right=None):
        cursor = self.conn.cursor()

        if not delta_time_to_left: 
            delta_time_to_left = "00:00"
        if not delta_time_to_right: 
            delta_time_to_right = "00:00"
        
        query = "INSERT INTO meeting(ccode, starttime, endtime, cdays) VALUES (%s, %s, %s, %s) RETURNING mid;"
        cursor.execute(query, (ccode, starttime, endtime, cdays))

        mid = cursor.fetchone()
        if mid and (delta_time_to_left != "00:00" or delta_time_to_right != "00:00" and cdays == "MJ"):
            self.updateAllMeetingTime(ccode, starttime, endtime, cdays, delta_time_to_left, delta_time_to_right, mid)

        self.conn.commit()
        return mid
    
    def updateMeetingByMid(self, mid, ccode, starttime, endtime, cdays, delta_time_to_left=None, delta_time_to_right=None):
        cursor = self.conn.cursor()

        if not delta_time_to_left: 
            delta_time_to_left = "00:00"
        if not delta_time_to_right: 
            delta_time_to_right = "00:00"

        query = "UPDATE meeting SET ccode = %s, starttime = %s, endtime = %s, cdays = %s WHERE mid = %s RETURNING mid;"
        cursor.execute(query, (ccode, starttime, endtime, cdays, mid))

        mid = cursor.fetchone()
        if mid and (delta_time_to_left != "00:00" or delta_time_to_right != "00:00" and cdays == "MJ"):
            self.updateAllMeetingTime(ccode, starttime, endtime, cdays, delta_time_to_left, delta_time_to_right, mid)

        self.conn.commit()
        return mid
    
    def updateAllMeetingTime(self, ccode, starttime, endtime, cdays, delta_time_to_left, delta_time_to_right, ignored_mid=-1):

        if not delta_time_to_left: 
            delta_time_to_left = "00:00"
        if not delta_time_to_right: 
            delta_time_to_right = "00:00"
    
        # print(delta_time_to_right, delta_time_to_left)
        delta_time_to_right = datetime.strptime(delta_time_to_right.split(":")[0] + ":" + delta_time_to_right.split(":")[1], "%H:%M")
        delta_time_to_left = datetime.strptime(delta_time_to_left.split(":")[0] + ":" + delta_time_to_left.split(":")[1], "%H:%M")

        cursor = self.conn.cursor()
        adjust_meeting_query = """
            UPDATE meeting SET starttime = starttime + %s::interval, endtime = endtime + %s::interval
            WHERE cdays = 'MJ' AND ((starttime >= %s) OR (endtime >= %s));
        """
        cursor.execute(adjust_meeting_query, (delta_time_to_right.time(), delta_time_to_right.time(), starttime, endtime))

        adjust_meeting_query = """
            UPDATE meeting SET starttime = starttime - %s::interval, endtime = endtime - %s::interval
            WHERE cdays = 'MJ' AND ((starttime <= %s) OR (endtime <= %s));
        """
        cursor.execute(adjust_meeting_query, (delta_time_to_left.time(), delta_time_to_left.time(), starttime, endtime))

        self.conn.commit()

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
        query = """
            SELECT m.mid, m.ccode, m.starttime, m.endtime, m.cdays, COUNT(s.sid) AS section_count 
            FROM meeting m 
            JOIN section s ON m.mid = s.mid 
            GROUP BY m.mid, m.ccode, m.starttime, m.endtime, m.cdays 
            ORDER BY section_count DESC 
            LIMIT 5;
        """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def deleteAllMeetingsWithInvalidTime(self):
        cursor = self.conn.cursor()
        findMeets_ToDelete_Cursor = self.conn.cursor()
        findmidsToDelete = "SELECT mid FROM meeting WHERE cdays = 'MJ' AND (starttime < '07:30:00' OR endtime > '19:45:00');"
        query = """
            DELETE FROM meeting
            WHERE cdays = 'MJ' AND (starttime < '07:30:00' OR endtime > '19:45:00');
        """
        findMeets_ToDelete_Cursor.execute(findmidsToDelete)
        cursor.execute(query)
        result = findMeets_ToDelete_Cursor.fetchone()
        self.conn.commit()
        if result is not None:
            mid = result[0]
            return mid
        else:
            return None

