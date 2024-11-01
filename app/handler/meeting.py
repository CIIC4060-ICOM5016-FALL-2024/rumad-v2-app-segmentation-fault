import re
from datetime import datetime
from flask import jsonify
from dao.meeting import MeetingDAO


class MeetingHandler:
    def mapToDict(self, tuple):
        result = {}
        result["mid"] = tuple[0]
        result["ccode"] = tuple[1]
        result["starttime"] = tuple[2].strftime("%H:%M:%S") if hasattr(tuple[2], 'strftime') else tuple[2]
        result["endtime"] = tuple[3].strftime("%H:%M:%S") if hasattr(tuple[3], 'strftime') else tuple[3]
        result["cdays"] = tuple[4]
        return result
    
    def getAllMeeting(self):
        result = []
        dao = MeetingDAO()
        temp = dao.getAllMeeting()
        
        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)

    def getMeetingByMid(self, mid):
        dao = MeetingDAO()
        result = dao.getMeetingByMid(mid)
        
        if result is not None:
            return jsonify(self.mapToDict(result))
        else:
            return "Not Found", 404
    
    def insertMeeting(self, meeting_json):
        if "ccode" not in meeting_json or "starttime" not in meeting_json or "endtime" not in meeting_json or "cdays" not in meeting_json:
            return "Missing required fields", 400
        
        ccode = meeting_json["ccode"]
        starttime = datetime.strptime(meeting_json["starttime"], "%H:%M:%S").strftime("%H:%M:%S")
        endtime = datetime.strptime(meeting_json["endtime"], "%H:%M:%S").strftime("%H:%M:%S")
        cdays = meeting_json["cdays"]
        
        dao = MeetingDAO()
        mid = dao.insertMeeting(ccode, starttime, endtime, cdays)
        temp = (mid, ccode, starttime, endtime, cdays)
        
        return self.mapToDict(temp), 201