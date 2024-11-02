from flask import jsonify
from dao.section import SectionDAO


class SectionHandler:
    def mapToDict(self, tuple):
        result = {}
        result["sid"] = tuple[0]
        result["roomid"] = tuple[1]
        result["cid"] = tuple[2]
        result["mid"] = tuple[3]
        result["semester"] = tuple[4]
        result["year"] = tuple[5]
        result["capacity"] = tuple[6]
        return result

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
            return "Not Found", 404

    def deleteSectionBySid(self, sid):
        dao = SectionDAO()
        if dao.deleteSectionBySid(sid):
            return jsonify(DeleteStatus="OK"), 200
        else:
            return jsonify(DeleteStatus="NOT FOUND"), 404