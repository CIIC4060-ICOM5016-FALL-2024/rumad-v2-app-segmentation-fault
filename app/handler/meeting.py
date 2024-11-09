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
        cdays = cdays.upper()
        if not ccode or not starttime or not endtime or not cdays:
            return jsonify(InsertStatus="Missing required fields"), 404
        if any(len(value.strip()) == 0 or not isinstance(value, str) for value in [ccode, cdays]):
            return jsonify(InsertStatus="A entry is empty or invalid type"), 400
        
        if cdays not in ["LMV", "MJ"]:
            return jsonify(InsertStatus="Invalid cdays"), 400 
        
        if (len(starttime.split(":")) == 1 and starttime.split(":")[0].isdigit()):
            starttime = starttime + ":00"
        if (len(endtime.split(":")) == 1 and endtime.split(":")[0].isdigit()):
            endtime = endtime + ":00"

        if (len(starttime.split(":")) == 3 and starttime.split(":")[2].isdigit()):
            starttime = starttime.split(":")[0] + ":" + starttime.split(":")[1]
        if (len(endtime.split(":")) == 3 and endtime.split(":")[2].isdigit()):
            endtime = endtime.split(":")[0] + ":" + endtime.split(":")[1]

        if (len(starttime.split(":")) > 3 or len(endtime.split(":")) > 3):
            return jsonify(InsertStatus="Invalid time format"), 400
        
        if not (len(starttime.split(":")) == 2 or len(starttime.split(":")) == 3) and (not (len(endtime.split(":")) == 2 or len(endtime.split(":")) == 3)):
            return jsonify(InsertStatus="Invalid time format"), 400

        
        if (not (starttime.split(":")[0].isdigit() and starttime.split(":")[1].isdigit() and endtime.split(":")[0].isdigit() and endtime.split(":")[1].isdigit())):    
            return jsonify(InsertStatus="Invalid time format"), 400
        
        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")
        
        if (starttime_dt >= endtime_dt or starttime_dt == endtime_dt or 
            starttime_dt < datetime.strptime("7:30", "%H:%M") 
            or endtime_dt > datetime.strptime("19:45", "%H:%M")):	
            return jsonify(InsertStatus="Invalid time range"), 400
        
        if cdays == "LMV" and not (endtime_dt - starttime_dt == timedelta(hours=0, minutes=50)):
            return jsonify(InsertStatus="Invalid time range for LMV meetings"), 400
        
        if cdays == "MJ" and not (endtime_dt - starttime_dt == timedelta(hours=1, minutes=15)):
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
        ccode = meeting_json["ccode"]
        starttime = meeting_json["starttime"]
        endtime = meeting_json["endtime"]
        cdays = meeting_json["cdays"]
        
        jsonify_error, error = self.validateMeetingInput(ccode, starttime, endtime, cdays)
        if error:
            return jsonify_error, error

        if len(starttime.split(":")) == 1:
            starttime = starttime + ":00"
        if len(endtime.split(":")) == 1:
            endtime = endtime + ":00"

        dao = MeetingDAO()
        if not dao.checkMeetingDuplicate(ccode, starttime, endtime, cdays):
            return jsonify(InsertStatus="Duplicate Meeting"), 404

        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")
        timedelta_12_30 = datetime.strptime("12:30", "%H:%M")
        timedelta_10_15 = datetime.strptime("10:15", "%H:%M")

        
        mid = None
        if(starttime_dt >= timedelta_10_15 and starttime_dt < timedelta_12_30):
            delta_time_to_right_dt =  timedelta_12_30 - starttime_dt
            starttime = str((starttime_dt + delta_time_to_right_dt).time())
            endtime = str((endtime_dt + delta_time_to_right_dt).time())
            mid = dao.insertMeeting(ccode, starttime, endtime, cdays, delta_time_to_right=str(delta_time_to_right_dt))
            dao.deleteAllMeetingsWithInvalidTime()
        
        elif(endtime_dt < timedelta_12_30 and endtime_dt > timedelta_10_15):
            delta_time_to_left_dt =  endtime_dt - timedelta_10_15
            starttime = str((starttime_dt - delta_time_to_left_dt).time())
            endtime = str((endtime_dt - delta_time_to_left_dt).time())
            mid = dao.insertMeeting(ccode, starttime, endtime, cdays, delta_time_to_left=str(delta_time_to_left_dt))   
            dao.deleteAllMeetingsWithInvalidTime()
                 
        else:
            mid = dao.insertMeeting(ccode, starttime, endtime, cdays)

        if mid:
            temp = (mid, ccode, starttime, endtime, cdays)
            return jsonify(self.mapToDict(temp)), 201
        else:
            return jsonify(InsertStatus="Error Inserting Meeting"), 400
        

    def deleteMeetingByMid(self, mid):
        dao = MeetingDAO()
        result = dao.deleteMeetingByMid(mid)
        if result:
            return jsonify(DeleteStatus="OK"), 200
        else:
            return jsonify(DeleteStatus="Not Found"), 404
        
    def updateMeetingByMid(self, mid, meeting_json):
        ccode = meeting_json["ccode"]
        starttime = meeting_json["starttime"]
        endtime = meeting_json["endtime"]
        cdays = meeting_json["cdays"]
        
        jsonify_error, error = self.validateMeetingInput(ccode, starttime, endtime, cdays)
        if error:
            return jsonify_error, error
        
        if len(starttime.split(":")) == 1:
            starttime = starttime + ":00"
        if len(endtime.split(":")) == 1:
            endtime = endtime + ":00"
        
        dao = MeetingDAO()
        if not dao.checkMeetingDuplicate(ccode, starttime, endtime, cdays):
            return jsonify(InsertStatus="Duplicate Meeting"), 404
        
        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")
        timedelta_12_30 = datetime.strptime("12:30", "%H:%M")
        timedelta_10_15 = datetime.strptime("10:15", "%H:%M")    

        if(starttime_dt >= timedelta_10_15 and starttime_dt < timedelta_12_30):
            delta_time_to_right_dt =  timedelta_12_30 - starttime_dt
            result = dao.updateMeetingByMid(mid, ccode, starttime, endtime, cdays, delta_time_to_right=str(delta_time_to_right_dt))
            dao.deleteAllMeetingsWithInvalidTime()

        elif(endtime_dt < timedelta_12_30 and endtime_dt > timedelta_10_15):
            delta_time_to_left_dt =  endtime_dt - timedelta_10_15
            result = dao.updateMeetingByMid(mid, ccode, starttime, endtime, cdays, delta_time_to_left=str(delta_time_to_left_dt))
            dao.deleteAllMeetingsWithInvalidTime()

        else:
            result = dao.updateMeetingByMid(mid, ccode, starttime, endtime, cdays)

        if result:
            return jsonify(UpdateStatus="OK"), 200
        else:
            return jsonify(UpdateStatus="Not Found"), 404