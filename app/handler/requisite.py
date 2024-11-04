from flask import jsonify
from dao.requisite import RequisiteDAO
from handler.data_validation import clean_data
import pandas as pd


class RequisiteHandler:
    def mapToDict(self, tuple):
        result = {}
        result["classid"] = tuple[0]
        result["reqid"] = tuple[1]
        result["prereq"] = tuple[2]
        return result

    def confirmDataInDF(self, df_to_verify, df_requisite):
        columns_to_check = ["classid", "reqid", "prereq"]
        df_requisite = df_requisite.astype({col: str for col in columns_to_check})
        df_to_verify = df_to_verify.astype({col: str for col in columns_to_check})

        # Check if the data to insert is already in the database
        values_to_check = df_to_verify[columns_to_check].iloc[0]
        duplicate_count = (df_requisite[columns_to_check].eq(values_to_check).all(axis=1).sum())

        return duplicate_count == 1

    def getAllRequisite(self):
        result = []
        dao = RequisiteDAO()
        temp = dao.getAllRequisite()

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)

    def getRequisiteByClassIdReqId(self, classid, reqid):
        dao = RequisiteDAO()
        result = dao.getRequisiteByClassIdReqId(classid, reqid)

        if result is not None:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify(GetStatus="NOT FOUND"), 404

    def insertRequisite(self, requisite_json):
        if (
            "classid" not in requisite_json
            or "reqid" not in requisite_json
            or "prereq" not in requisite_json
        ):
            return jsonify(InsertStatus="Missing required fields"), 400

        classid = requisite_json["classid"]
        reqid = requisite_json["reqid"]
        prereq = requisite_json["prereq"]

        data = {"classid": [classid], "reqid": [reqid], "prereq": [prereq]}
        df_to_insert = pd.DataFrame(data)
        df_list = clean_data(df_to_insert, "requisite")

        df_requisite = []
        for df, df_name in df_list:
            if df_name == "requisite":
                df_requisite = df

        is_data_confirmed = self.confirmDataInDF(df_to_insert, df_requisite)

        if is_data_confirmed:
            dao = RequisiteDAO()
            ids = dao.insertRequisite(classid, reqid, prereq)
            temp = (ids[0], ids[1], prereq)  # type: ignore

            return self.mapToDict(temp), 201
        else:
            return jsonify(InsertStatus="Duplicate Entry"), 400

    def deleteRequisiteByClassIdReqId(self, classid, reqid):
        dao = RequisiteDAO()
        if dao.deleteRequisiteByClassIdReqId(classid, reqid):
            return jsonify(DeleteStatus="OK"), 200
        else:
            return jsonify(DeleteStatus="NOT FOUND"), 404

    def updateRequisiteByClassIdReqId(self, classid, reqid, requisite_json):
        if "prereq" not in requisite_json:
            return jsonify(InsertStatus="Missing required fields"), 400

        prereq = requisite_json["prereq"]

        dao = RequisiteDAO()
        if dao.getRequisiteByClassIdReqId(classid, reqid) is None:
            return jsonify(UpdateStatus="NOT FOUND"), 404
        else:
            dao.updateRequisiteByClassIdReqId(classid, reqid, prereq)
            temp = (classid, reqid, prereq)
            return jsonify(self.mapToDict(temp)), 200
