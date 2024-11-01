import re
from flask import jsonify
from numpy import insert
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
        
    def insertRequisite(self, requisite_json):
        if "classid" not in requisite_json or "reqid" not in requisite_json or "prereq" not in requisite_json:
            return "Missing required fields", 400
    
        classid = requisite_json["classid"]
        reqid = requisite_json["reqid"]
        prereq = requisite_json["prereq"]
        
        dao = RequisiteDAO()
        ids = dao.insertRequisite(classid, reqid, prereq)
        temp = (ids[0], ids[1], prereq)  # type: ignore
        
        return self.mapToDict(temp), 201
        
        
