import pandas as pd
from datetime import datetime
from flask import jsonify
from dao.meeting import MeetingDAO
from handler.insert_update_handler import clean_data


class MeetingHandler:
    def mapToDict(self, tuple):
        result = {}
        result["mid"] = tuple[0]
        result["ccode"] = tuple[1]
        result["starttime"] = tuple[2].strftime("%H:%M:%S") if hasattr(tuple[2], 'strftime') else tuple[2]
        result["endtime"] = tuple[3].strftime("%H:%M:%S") if hasattr(tuple[3], 'strftime') else tuple[3]
        result["cdays"] = tuple[4]
        return result
    
    def confirmDataInDF(self, df_to_verify, df_meeting):
        # Check for duplicates in df_meeting based on columns except 'mid'
        columns_to_check = [col for col in df_to_verify.columns if col != "mid"]
        values_to_check = df_to_verify[columns_to_check].iloc[0]
        duplicates = df_meeting[columns_to_check].eq(values_to_check).all(axis=1).any()
        
        if duplicates:
            return False
        
        # If no duplicates, check if 'mid' in df_to_verify exists in df_meeting
        mid_value = df_to_verify["mid"].values[0]
        if mid_value in df_meeting["mid"].values:
            return True
        else:
            return False

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
        
        data = {
            "mid": 1000,
            "ccode": [ccode],
            "starttime": [starttime],
            "endtime": [endtime],
            "cdays": [cdays]
        }
        df_to_insert = pd.DataFrame(data)
        df_list = clean_data(df_to_insert, "meeting")
        
        df_meeting = []
        for df, df_name in df_list:
            if df_name == "meeting":
                df_meeting = df
                print(df_meeting)
                
        is_data_confirmed = self.confirmDataInDF(df_to_insert, df_meeting)
        
        if is_data_confirmed:
            dao = MeetingDAO()
            mid = dao.insertMeeting(ccode, starttime, endtime, cdays)
            temp = (mid, ccode, starttime, endtime, cdays)
            
            return self.mapToDict(temp), 201
        
        else:
            return "Data cant be inserted", 400