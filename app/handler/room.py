import pandas as pd
from flask import jsonify
from dao.room import RoomDAO
from handler.data_validation import clean_data



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
        
        data = {
            "rid": 1000,
            "building": [building],
            "room_number": [room_number],
            "capacity": [capacity]
        }
        df_to_insert = pd.DataFrame(data)
        df_list = clean_data(df_to_insert, "room")
        
        df_room = []
        for df, df_name in df_list:
            if df_name == "room":
                df_room = df
                
        is_data_confirmed = self.confirmDataInDF(df_to_insert, df_room)
        
        if is_data_confirmed:
            dao = RoomDAO()
            rid = dao.insertRoom(building, room_number, capacity)
            temp = (rid, building, room_number, capacity)
            return jsonify(self.mapToDict(temp)), 201
        else:
            return jsonify(InsertStatus = "Data can't be inserted due to duplicates or invalid data"), 400

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
        
        data = {
            "rid": 1000,
            "building": [building],
            "room_number": [room_number],
            "capacity": [capacity]
        }
        df_to_update = pd.DataFrame(data)
        df_list = clean_data(df_to_update, "room")
        
        df_room = []
        for df, df_name in df_list:
            if df_name == "room":
                df_room = df
                
        is_data_confirmed = self.confirmDataInDF(df_to_update, df_room)
        
        if is_data_confirmed:
            temp = dao.updateRoomByRid(rid, building, room_number, capacity)
            if temp:
                tup = (rid, building, room_number, capacity)
                return jsonify(self.mapToDict(tup)), 200
            else:
                return jsonify(UpdateStatus="NOT FOUND"), 404
        else:
            return jsonify(UpdateStatus = "Data can't be updated due to duplicates or invalid data"), 400






