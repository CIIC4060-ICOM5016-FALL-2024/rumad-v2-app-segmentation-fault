from flask import jsonify
from dao.requisite import RequisiteDAO


class RequisiteHandler:
    def mapToDict(self, tuple):
        result = {}
        result["classid"] = tuple[0]
        result["reqid"] = tuple[1]
        result["prereq"] = tuple[2]
        return result

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
            return "Not Found", 404

    def deleteRequisiteByClassIdReqId(self, classid, reqid):
        dao = RequisiteDAO()
        if dao.deleteRequisiteByClassIdReqId(classid, reqid):
            return jsonify(DeleteStatus="OK"), 200
        else:
            return jsonify(DeleteStatus="NOT FOUND"), 404
