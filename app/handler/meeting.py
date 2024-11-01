import re
from flask import jsonify
from dao.meeting import MeetingDAO


class MeetingHandler:
    def mapToDict(self, tuple):
        result = {}
        result["mid"] = tuple[0]
        result["ccode"] = tuple[1]
        result["starttime"] = tuple[2].strftime("%H:%M:%S")
        result["endtime"] = tuple[3].strftime("%H:%M:%S")
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
