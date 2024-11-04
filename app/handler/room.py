from flask import jsonify
from dao.room import RoomDAO
from handler.course import ClassHandler


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

    def insertRoom(self, room_json):
        building = room_json["building"]
        room_number = room_json["room_number"]
        capacity = room_json["capacity"]
        dao = RoomDAO()
        rid = dao.insertRoom(building, room_number, capacity)
        temp = (rid, building, room_number, capacity)
        return jsonify(self.mapToDict(temp)), 201

    def deleteRoomByRid(self, rid):
        dao = RoomDAO()
        result = dao.deleteRoomByRid(rid)
        if result:
            return jsonify(DeleteStatus="OK"), 200
        else:
            return jsonify(DeleteStatus="Not Found"), 404

    def updateRoomByRid(self, rid, room_json):
        building = room_json["building"]
        room_number = room_json["room_number"]
        capacity = room_json["capacity"]
        dao = RoomDAO()
        temp = dao.updateRoomByRid(rid, building, room_number, capacity)
        if temp:
            tup = (rid, building, room_number, capacity)
            return jsonify(self.mapToDict(tup)), 200
        else:
            return jsonify(UpdateStatus="Not Found"), 404

    def getMaxCapacity(self, building):
        result = []
        dao = RoomDAO()
        temp = dao.getMaxCapacity(building)
        if temp:
            for item in temp:
                result.append(self.mapToDict(item))
            return jsonify(result), 200
        else:
            return jsonify(UpdateStatus="Not Found"), 404
        
    def getRatioByBuilding(self, building):
        result = []
        dao = RoomDAO()
        temp = dao.getRatioByBuilding(building)
        if temp:
            for item in temp:
                result.append(self.mapToDict(item))
            return jsonify(result), 200
        else:
            return jsonify(UpdateStatus="Not Found"), 404
        
    def getMostClassesByRid(self, rid):
        result = []
        dao = RoomDAO()
        class_handler = ClassHandler()
        temp = dao.getMostClassesByRid(rid)
        if temp:
            for item in temp:
                result.append(class_handler.mapToDict(item))
            return jsonify(result), 200
        else:
            return jsonify(UpdateStatus="Not Found"), 404
    








