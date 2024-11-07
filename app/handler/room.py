from flask import jsonify
from dao.room import RoomDAO


class RoomHandler:
    def mapToDict(self, tuple):
        result = {
            "rid": tuple[0],
            "building": tuple[1],
            "room_number": tuple[2],
            "capacity": tuple[3],
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

        if not building or not room_number or not capacity:
            return jsonify(InsertStatus="Missing required fields"), 404
        if not isinstance(capacity, int) or capacity <= 0:
            return jsonify(InsertStatus="Invalid capacity"), 404

        if any(
            len(value.strip()) == 0 or not isinstance(value, str)
            for value in [building, room_number]
        ):
            return jsonify(InsertStatus="A entry is empty or invalid type"), 400

        dao = RoomDAO()
        rid = dao.insertRoom(building, room_number, capacity)
        if rid:
            temp = (rid, building, room_number, capacity)
            return jsonify(self.mapToDict(temp)), 201
        else:
            return jsonify(InsertStatus="Duplicate Room"), 404

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

        if not building or not room_number or not capacity:
            return jsonify(UpdateStatus="Missing required fields"), 404
        if not isinstance(capacity, int) or capacity <= 0:
            return jsonify(UpdateStatus="Invalid capacity"), 404

        if any(
            len(value.strip()) == 0 or not isinstance(value, str)
            for value in [building, room_number]
        ):
            return jsonify(InsertStatus="A entry is empty or invalid type"), 400

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
