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
        
        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")
        
        if (starttime_dt >= endtime_dt or starttime_dt == endtime_dt or 
            starttime_dt < datetime.strptime("7:30", "%H:%M") 
            or endtime_dt > datetime.strptime("19:45", "%H:%M")):	
            return jsonify(InsertStatus="Invalid time range"), 400
        
        if cdays == "LMV" and not (endtime_dt - starttime_dt == timedelta(hours=0, minutes=50)):
            return jsonify(InsertStatus="Invalid time range for LMV meetings"), 400
        
        print((endtime_dt - starttime_dt))
        print(timedelta(hours=1, minutes=15))
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

        starttime_dt = datetime.strptime(starttime.split(":")[0] + ":" + starttime.split(":")[1], "%H:%M")
        endtime_dt = datetime.strptime(endtime.split(":")[0] + ":" + endtime.split(":")[1], "%H:%M")
        timedelta_12_30 = datetime.strptime("12:30", "%H:%M")
        timedelta_10_15 = datetime.strptime("10:15", "%H:%M")

        dao = MeetingDAO()
        mid = None
        if(starttime_dt >= timedelta_10_15 and starttime_dt < timedelta_12_30):
            delta_time_to_right =  str(timedelta_12_30 - starttime_dt)
            starttime = (starttime_dt + timedelta(hours=int(delta_time_to_right.split(':')[0]), minutes=int(delta_time_to_right.split(':')[1]), seconds=0)).strftime("%H:%M:%S")
            endtime = (starttime_dt + timedelta(hours=int(delta_time_to_right.split(':')[0]), minutes=int(delta_time_to_right.split(':')[1]), seconds=0)).strftime("%H:%M:%S")
            mid = dao.insertMeetingAndDisplaceByTimeAmout(ccode, starttime, endtime, cdays, delta_time_to_left="00:00", delta_time_to_right=delta_time_to_right)
        
        elif(endtime_dt < timedelta_12_30 and endtime_dt > timedelta_10_15):
            delta_time_to_left =  str(endtime_dt - timedelta_10_15)
            starttime = (starttime - timedelta(hours=int(delta_time_to_left.split(':')[0]), minutes=int(delta_time_to_left.split(':')[1]), seconds=0)).strftime("%H:%M:%S")
            endtime = (endtime_dt - timedelta(hours=int(delta_time_to_left.split(':')[0]), minutes=int(delta_time_to_left.split(':')[1]), seconds=0)).strftime("%H:%M:%S")
            mid = dao.insertMeetingAndDisplaceByTimeAmout(ccode, starttime, endtime, cdays, delta_time_to_left=delta_time_to_left, delta_time_to_right="00:00")
        
        else:
            mid = dao.insertMeeting(ccode, starttime, endtime, cdays)

        if mid:
            temp = (mid, ccode, starttime, endtime, cdays)
            return jsonify(self.mapToDict(temp)), 201
        else:
            return jsonify(InsertStatus="Duplicate Meeting"), 404
        

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
        
        if not ccode or not starttime or not endtime or not cdays:
            return jsonify(UpdateStatus="Missing required fields"), 404
        if any(len(value.strip()) == 0 or not isinstance(value, str) for value in [ccode, cdays]):
            return jsonify(UpdateStatus="A entry is empty or invalid type"), 400

        dao = MeetingDAO()
        result = dao.updateMeetingByMid(mid, ccode, starttime, endtime, cdays)
        if result:
            return jsonify(UpdateStatus="OK"), 200
        else:
            return jsonify(UpdateStatus="Not Found"), 404