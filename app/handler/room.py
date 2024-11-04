import pandas as pd
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
    
    def confirmDataInDF(self, df_to_verify, df_meeting):
        columns_to_check = ["building", "room_number", "capacity"]
        df_meeting = df_meeting.astype({col: str for col in columns_to_check})
        df_to_verify = df_to_verify.astype({col: str for col in columns_to_check})

        # Check if the data to insert is already in the database
        values_to_check = df_to_verify[columns_to_check].iloc[0]
        duplicate_count = (df_meeting[columns_to_check].eq(values_to_check).all(axis=1).sum())

        return duplicate_count == 1

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
            return jsonify(GetStatus="Not Found"), 404

    def insertRoom(self, room_json):
        if ("building" not in room_json or "room_number" not in room_json or "capacity" not in room_json):
            return jsonify(InsertStatus="Missing required fields"), 400
        
        building = room_json["building"]
        room_number = room_json["room_number"]
        capacity = room_json["capacity"]

        if not building or not room_number or not capacity:
            return jsonify(InsertStatus="Missing required fields"), 404
        if not isinstance(capacity, int)  or capacity <= 0:
            return jsonify(InsertStatus="Invalid capacity"), 404
        if not isinstance(room_number, str) or len(room_number) == 0:
            return jsonify(InsertStatus="Invalid room_number"), 404
        if not isinstance(building, str) or len(building) == 0:
            return jsonify(InsertStatus="Invalid building"), 404
        
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
            return jsonify(DeleteStatus="NOT FOUND"), 404

    def updateRoomByRid(self, rid, room_json):
        dao = RoomDAO()
        if not dao.getRoomByRid(rid):
            return jsonify(UpdateStatus="NOT FOUND"), 404
        
        if ("building" not in room_json or "room_number" not in room_json or "capacity" not in room_json):
            return jsonify(UpdateStatus="Missing required fields"), 400
        
        building = room_json["building"]
        room_number = room_json["room_number"]
        capacity = room_json["capacity"]

        if not building or not room_number or not capacity:
            return jsonify(UpdateStatus="Missing required fields"), 404
        if not isinstance(capacity, int)  or capacity <= 0:
            return jsonify(UpdateStatus="Invalid capacity"), 404
        if not isinstance(room_number, str) or len(room_number) == 0:
            return jsonify(UpdateStatus="Invalid room_number"), 404
        if not isinstance(building, str) or len(building) == 0:
            return jsonify(UpdateStatus="Invalid building"), 404
        
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
        
    








