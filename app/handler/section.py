from flask import jsonify
import pandas as pd
from handler.data_validation import clean_data
from dao.section import SectionDAO


class SectionHandler:
    def mapToDict(self, tuple):
        result = {}
        result["sid"] = tuple[0]
        result["roomid"] = tuple[1]
        result["cid"] = tuple[2]
        result["mid"] = tuple[3]
        result["semester"] = tuple[4]
        result["years"] = tuple[5]
        result["capacity"] = tuple[6]
        return result

    def confirmDataInDF(self, df_to_verify, df_section):
        columns_to_check = ["roomid", "cid", "mid", "semester", "years"]
        df_section = df_section.astype({col: str for col in columns_to_check})
        df_to_verify = df_to_verify.astype({col: str for col in columns_to_check})

        # Check if the data to insert is already in the database
        values_to_check = df_to_verify[columns_to_check].iloc[0]
        duplicate_count = (
            df_section[columns_to_check].eq(values_to_check).all(axis=1).sum()
        )

        return duplicate_count == 1

    def getAllSection(self):
        result = []
        dao = SectionDAO()
        temp = dao.getAllSection()

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)

    def getSectionBySid(self, sid):
        dao = SectionDAO()
        result = dao.getSectionBySid(sid)

        if result is not None:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify(GetStatus="NOT FOUND"), 404

    def insertSection(self, section_json):
        if (
            "roomid" not in section_json
            or "cid" not in section_json
            or "mid" not in section_json
            or "semester" not in section_json
            or "years" not in section_json
            or "capacity" not in section_json
        ):
            return jsonify(InsertStatus="Missing required fields"), 400

        roomid = section_json["roomid"]
        cid = section_json["cid"]
        mid = section_json["mid"]
        semester = section_json["semester"]
        years = section_json["years"]
        capacity = section_json["capacity"]

        if not isinstance(roomid, int):
            return jsonify(InsertStatus="Invalid datatype roomid"), 400
        if not isinstance(cid, int):
            return jsonify(InsertStatus="Invalid datatype cid"), 400
        if not isinstance(mid, int):
            return jsonify(InsertStatus="Invalid datatype mid"), 400
        if not isinstance(semester, str):
            return jsonify(InsertStatus="Invalid datatype semester"), 400
        if not isinstance(years, str):
            return jsonify(InsertStatus="Invalid datatype years"), 400
        if not isinstance(capacity, int):
            return jsonify(InsertStatus="Invalid datatype capacity"), 400
        if capacity <= 0:
            return jsonify(InsertStatus="Capacity less than 1"), 400

        # Verify str length of all values
        if any(len(value.strip()) == 0 for value in [semester, years]):
            return jsonify(UpdateStatus="A entry is empty"), 400

        if any(len(value.strip()) > 4 for value in [years]):
            return jsonify(UpdateStatus="Invalid years"), 400

        data = {
            "sid": 1000,
            "roomid": [roomid],
            "cid": [cid],
            "mid": [mid],
            "semester": [semester],
            "years": [years],
            "capacity": [capacity],
        }
        df_to_insert = pd.DataFrame(data)

        dao = SectionDAO()
        columns = ["sid", "roomid", "cid", "mid", "semester", "years", "capacity"]
        df_section = pd.DataFrame(dao.getAllSection(), columns=columns)
        df_section = pd.concat([df_section, df_to_insert], ignore_index=True)

        not_duplicate = self.confirmDataInDF(df_to_insert, df_section)

        if not not_duplicate:
            return jsonify(InsertStatus="Duplicate Entry"), 400

        df_list = clean_data(df_to_insert, "section")

        df_section = []
        for df, df_name in df_list:
            if df_name == "section":
                df_section = df

        is_data_confirmed = self.confirmDataInDF(df_to_insert, df_section)

        if is_data_confirmed:
            dao = SectionDAO()
            sid = dao.insertSection(roomid, cid, mid, semester, years, capacity)
            temp = (sid, roomid, cid, mid, semester, years, capacity)

            return self.mapToDict(temp), 201
        else:
            return jsonify(InsertStatus="Invalid data"), 400

    def deleteSectionBySid(self, sid):
        dao = SectionDAO()
        if dao.deleteSectionBySid(sid):
            return jsonify(DeleteStatus="OK"), 200
        else:
            return jsonify(DeleteStatus="NOT FOUND"), 404

    def updateSectionBySid(self, sid, section_json):
        if (
            "roomid" not in section_json
            or "cid" not in section_json
            or "mid" not in section_json
            or "semester" not in section_json
            or "years" not in section_json
            or "capacity" not in section_json
        ):
            return jsonify(UpdateStatus="Missing required fields"), 400

        roomid = section_json["roomid"]
        cid = section_json["cid"]
        mid = section_json["mid"]
        semester = section_json["semester"]
        years = section_json["years"]
        capacity = section_json["capacity"]

        if not isinstance(roomid, int):
            return jsonify(InsertStatus="Invalid datatype roomid"), 400
        if not isinstance(cid, int):
            return jsonify(InsertStatus="Invalid datatype cid"), 400
        if not isinstance(mid, int):
            return jsonify(InsertStatus="Invalid datatype mid"), 400
        if not isinstance(semester, str):
            return jsonify(InsertStatus="Invalid datatype semester"), 400
        if not isinstance(years, str):
            return jsonify(InsertStatus="Invalid datatype years"), 400
        if not isinstance(capacity, int):
            return jsonify(InsertStatus="Invalid datatype capacity"), 400
        if capacity <= 0:
            return jsonify(InsertStatus="Capacity less than 1"), 400

        # Verify str length of all values
        if any(len(value.strip()) == 0 for value in [semester, years]):
            return jsonify(UpdateStatus="A entry is empty"), 400

        if any(len(value.strip()) > 4 for value in [years]):
            return jsonify(UpdateStatus="Invalid years"), 400

        data = {
            "sid": 1000,
            "roomid": [roomid],
            "cid": [cid],
            "mid": [mid],
            "semester": [semester],
            "years": [years],
            "capacity": [capacity],
        }
        df_to_update = pd.DataFrame(data)

        dao = SectionDAO()
        columns = ["sid", "roomid", "cid", "mid", "semester", "years", "capacity"]
        df_section = pd.DataFrame(dao.getAllSection(), columns=columns)
        # Exclude the current section from the duplicate check
        df_section = df_section[df_section["sid"] != sid]

        df_section = pd.concat([df_section, df_to_update], ignore_index=True)

        not_duplicate = self.confirmDataInDF(df_to_update, df_section)

        if not not_duplicate:
            return jsonify(InsertStatus="Duplicate Entry"), 400

        df_list = clean_data(df_to_update, "section")

        df_section = []
        for df, df_name in df_list:
            if df_name == "section":
                df_section = df

        is_data_confirmed = self.confirmDataInDF(df_to_update, df_section)

        if is_data_confirmed:
            if dao.updateSectionBySid(sid, roomid, cid, mid, semester, years, capacity):
                return jsonify(UpdateStatus="OK"), 200
            else:
                return jsonify(UpdateStatus="NOT FOUND"), 404

        else:
            return jsonify(UpdateStatus="Invalid data"), 400

    def getSectionPerYear(self):
        dao = SectionDAO()
        result = dao.getSectionPerYear()

        if result is not None:
            return jsonify(result)
        else:
            return jsonify(GetStatus="NOT FOUND"), 404

    def getRatioByBuilding(self, building):
        result = []
        dao = SectionDAO()
        temp = dao.getRatioByBuilding(building)
        if temp:
            for item in temp:
                result.append(self.mapToDict(item))
            return jsonify(result), 200
        else:
            return jsonify(UpdateStatus="Not Found"), 404
