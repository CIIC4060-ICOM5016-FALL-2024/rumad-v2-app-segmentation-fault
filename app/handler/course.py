from Flask import jsonify
from dao.course import ClassDAO


class ClassHandler:
    def mapToDict(self, tuple):
        result = {}
        result['cid'] = tuple[0]
        result['cname'] = tuple[1]
        result['ccode'] = tuple[2]
        result['cdesc'] = tuple[3]
        result['term'] = tuple[4]
        result['years'] = tuple[5]
        result['cred'] = tuple[6]
        result['csyllabus'] = tuple[7]
        return result

    def getAllClass(self):
        result = []
        dao = ClassDAO()
        temp = dao.getAllClass

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)
