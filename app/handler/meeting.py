from flask import jsonify
from datetime import datetime, timedelta
from dao.meeting import MeetingDAO

class MeetingHandler:
    def mapToDict(self, tuple):
        result = {}
        result["mid"] = tuple[0]
        result["ccode"] = tuple[1]
        result["starttime"] = (tuple[2].strftime("%H:%M:%S") if hasattr(tuple[2], "strftime") else tuple[2])
        result["endtime"] = (tuple[3].strftime("%H:%M:%S") if hasattr(tuple[3], "strftime") else tuple[3])
        result["cdays"] = tuple[4]
        return result
    
    def validateMeetingInput(self, ccode, starttime, endtime, cdays):
        if not ccode or not starttime or not endtime or not cdays:
            return jsonify(InsertStatus="Missing required fields"), 404
        
        if any(
            not isinstance(value, str) for value in [ccode, starttime, endtime, cdays]
        ) or any(
            len(value.strip()) == 0 for value in [ccode, starttime, endtime, cdays]
        ):
            return jsonify(InsertStatus="A entry is empty or invalid type"), 400
        
        cdays = cdays.upper()
        if cdays not in ["LWV", "MJ"]:
            return jsonify(InsertStatus="Invalid cdays"), 400 
        
        starttime_dt = endtime_dt = None
        try:
             starttime_dt = datetime.strptime(starttime, "%H:%M:%S")
        except ValueError:
            return jsonify(InsertStatus="Invalid datetime format for starttime"), 400

        try:
            endtime_dt = datetime.strptime(endtime, "%H:%M:%S")
        except ValueError:
            return jsonify(InsertStatus="Invalid datetime format for endtime"), 400
        
        if(starttime_dt.second != 0 or endtime_dt.second != 0):
            return jsonify(InsertStatus="Seconds should be 0"), 400

        if (starttime_dt >= endtime_dt or starttime_dt == endtime_dt):	
            return jsonify(InsertStatus="Invalid time range, starttime is the same or more than endtime"), 400
        
        if (cdays == "MJ" and (starttime_dt < datetime.strptime("7:30", "%H:%M") or endtime_dt > datetime.strptime("19:45", "%H:%M"))):
            return jsonify(InsertStatus="Invalid time range"), 400
        
        if (cdays == "MJ" and (starttime_dt >= datetime.strptime("10:15", "%H:%M") and endtime_dt <= datetime.strptime("12:30", "%H:%M"))):
            return jsonify(InsertStatus="Invalid time range for MJ meetings, 'Hora Universal'"), 400
        
        if cdays == "LWV" and not (endtime_dt - starttime_dt == timedelta(hours=0, minutes=50, seconds=0)):
            return jsonify(InsertStatus="Invalid time range for LMV meetings"), 400
        
        if cdays == "MJ" and not (endtime_dt - starttime_dt == timedelta(hours=1, minutes=15, seconds=0)):
            return jsonify(InsertStatus="Invalid time range for MJ meetings"), 400
        
        return None, None

    def getAllMeeting(self):
        result = []
        dao = MeetingDAO()
        temp = dao.getAllMeeting()
        for item in temp:
            result.append(self.mapToDict(item))
        return jsonify(result)
    
    def getMeetingByMid(self, mid):
        dao = MeetingDAO()
        result = dao.getMeetingByMid(mid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return "Not Found", 404
        
    def insertMeeting(self, meeting_json):
        if "ccode" not in meeting_json or "starttime" not in meeting_json or "endtime" not in meeting_json or "cdays" not in meeting_json:
            return jsonify(InsertStatus="Missing required fields"), 404
        
        ccode = meeting_json["ccode"]
        starttime = meeting_json["starttime"]
        endtime = meeting_json["endtime"]
        cdays = meeting_json["cdays"]
        
        jsonify_error, error = self.validateMeetingInput(ccode, starttime, endtime, cdays)
        if error:
            return jsonify_error, error

        dao = MeetingDAO()
        mid_temp = dao.checkMeetingDuplicate(ccode, starttime, endtime, cdays)
        if mid_temp:
            return jsonify(InsertStatus=f"Duplicate Meeting, meeting id: {mid[0]}"), 404

        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")
        timedelta_12_30 = datetime.strptime("12:30", "%H:%M")
        timedelta_10_15 = datetime.strptime("10:15", "%H:%M")

        starttime_temp, endtime_temp = starttime, endtime
        delta_time_to_left_str = delta_time_to_right_str = None  

        meetings_conflict = dao.checkMeetingConflict(starttime, endtime, cdays)


        if(starttime_dt >= timedelta_10_15 and starttime_dt < timedelta_12_30 and cdays == "MJ"):
            delta_time_to_right =  timedelta_12_30 - starttime_dt
            delta_time_to_right_str = str(delta_time_to_right)
            starttime_temp = str((starttime_dt + delta_time_to_right).time())
            endtime_temp = str((endtime_dt + delta_time_to_right).time())
            mid_temp = dao.checkMeetingDuplicate(ccode, starttime_temp, endtime_temp, cdays)
            if mid_temp:
                return jsonify(InsertStatus=f"Meeting conflict with meeting at 12:30pm, meeting id: {mid[0]}"), 400
        
        elif(endtime_dt < timedelta_12_30 and endtime_dt > timedelta_10_15 and cdays == "MJ"):
            delta_time_to_left =  endtime_dt - timedelta_10_15
            delta_time_to_left_str = str(delta_time_to_left)
            starttime_temp = str((starttime_dt - delta_time_to_left).time())
            endtime_temp = str((endtime_dt - delta_time_to_left).time())
            mid_temp = dao.checkMeetingDuplicate(ccode, starttime_temp, endtime_temp, cdays)
            if mid_temp:
                return jsonify(InsertStatus=f"Meeting conflict with meeting at 9:00am, meeting id: {mid[0]}"), 400
            
        elif(meetings_conflict):
            result = []
            for item in meetings_conflict:
                result.append(self.mapToDict(item))
            return jsonify(InsertStatus="Meeting conflict", conflict=result), 400

                 
        mid = dao.insertMeeting(ccode, starttime, endtime, cdays, delta_time_to_left=delta_time_to_left_str, delta_time_to_right=delta_time_to_right_str)
        mid_To_Delete = dao.deleteAllMeetingsWithInvalidTime()
        if mid_To_Delete is not None:
            return jsonify(InsertStatus="OK, This insert delete the meetings with 'ids' %s" % (mid_To_Delete)), 200

        if mid:
            temp = (mid, ccode, starttime_temp, endtime_temp, cdays)
            return jsonify(self.mapToDict(temp)), 201
        else:
            return jsonify(InsertStatus="Error Inserting Meeting"), 400
        
        
    def updateMeetingByMid(self, mid, meeting_json):
        if "ccode" not in meeting_json or "starttime" not in meeting_json or "endtime" not in meeting_json or "cdays" not in meeting_json:
            return jsonify(InsertStatus="Missing required fields"), 404
        
        ccode = meeting_json["ccode"]
        starttime = meeting_json["starttime"]
        endtime = meeting_json["endtime"]
        cdays = meeting_json["cdays"]
                
        jsonify_error, error = self.validateMeetingInput(ccode, starttime, endtime, cdays)
        if error:
            return jsonify_error, error
        
        dao = MeetingDAO()
        mid_temp = dao.checkMeetingDuplicate(ccode, starttime, endtime, cdays)
        if mid_temp:
            return jsonify(InsertStatus=f"Duplicate Meeting {mid}"), 404
        
        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")
        timedelta_12_30 = datetime.strptime("12:30", "%H:%M")
        timedelta_10_15 = datetime.strptime("10:15", "%H:%M")  

        delta_time_to_left = delta_time_to_right = None  
        delta_time_to_left_str = delta_time_to_right_str = None  

        meetings_conflict = dao.checkMeetingConflict(starttime, endtime, cdays)

        if(starttime_dt >= timedelta_10_15 and starttime_dt < timedelta_12_30 and cdays == "MJ"):
            delta_time_to_right =  timedelta_12_30 - starttime_dt
            delta_time_to_right_str = str(delta_time_to_right)
            mid_temp = dao.checkMeetingDuplicate(ccode, str(starttime_dt + delta_time_to_right), str(endtime_dt + delta_time_to_right), cdays)
            if mid_temp:
                return jsonify(InsertStatus=f"Meeting conflict with meeting at 12:30pm, meeting id: {mid_temp[0]}"), 404   

        elif(endtime_dt < timedelta_12_30 and endtime_dt > timedelta_10_15 and cdays == "MJ"):
            delta_time_to_left =  endtime_dt - timedelta_10_15
            delta_time_to_left_str = str(delta_time_to_left)
            mid_temp = dao.checkMeetingDuplicate(ccode, str(starttime_dt - delta_time_to_left), str(endtime_dt - delta_time_to_left), cdays)
            if mid_temp:
                return jsonify(InsertStatus=f"Meeting conflict with meeting at 9:00am, meetingid: {mid_temp[0]}"), 404
            
        elif(meetings_conflict):
            result = []
            for item in meetings_conflict:
                result.append(self.mapToDict(item))
            return jsonify(InsertStatus="Meeting conflict", conflict=result), 400
            

        # print("delta1:", delta_time_to_left, delta_time_to_right)
        result = dao.updateMeetingByMid(mid, ccode, starttime, endtime, cdays, delta_time_to_left=delta_time_to_left_str, delta_time_to_right=delta_time_to_right_str)

        mid_To_Delete = dao.deleteAllMeetingsWithInvalidTime()
        if mid_To_Delete is not None:
            return jsonify(InsertStatus="OK, This insert delete the meetings with 'ids' %s" % (mid_To_Delete)), 200

        if result:
            return jsonify(UpdateStatus="OK"), 200
        else:
            return jsonify(UpdateStatus="Not Found"), 404
        
    def deleteMeetingByMid(self, mid):
        dao = MeetingDAO()
        result = dao.deleteMeetingByMid(mid)
        if result:
            return jsonify(DeleteStatus="OK"), 200
        else:
            return jsonify(DeleteStatus="Not Found"), 404