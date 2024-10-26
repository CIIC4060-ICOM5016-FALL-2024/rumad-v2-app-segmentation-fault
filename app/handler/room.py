from flask import jsonify
from dao.room import RoomDAO


class RoomHandler:
    def mapToDict(self, tuple):
        result = {
            "rid" : tuple[0],
            "building" : tuple[1],
            "room_number" : tuple[2],
            "capacity" : tuple[3]
        }
        return result

    def getAllRoom(self):
        result = []
        dao = RoomDAO()
        temp = dao.getAllRoom()
        for item in temp:
            result.append(self.mapToDict(item))
        return jsonify(result)

    def getRoomByRid(self, rid):
        dao = RoomDAO()
        result = dao.getRoomByRid(rid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return "Not Found", 404



