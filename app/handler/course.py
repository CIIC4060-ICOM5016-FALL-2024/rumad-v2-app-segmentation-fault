from flask import jsonify
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
        temp = dao.getAllClass()

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)
    
    def getclassById(self, cid):
        dao = ClassDAO()
        temp = dao.getClassById(cid)
        if not temp:
            return jsonify(Error="Class Not Found"), 404
        else:
            result = self.mapToDict(temp)
            return jsonify(result)
    
    def insertClass(self, class_json):
        dao = ClassDAO()
        cname = class_json['cname']
        ccode = class_json['ccode']
        cdesc = class_json['cdesc']
        term = class_json['term']
        years = class_json['years']
        cred = class_json['cred']
        csyllabus = class_json['csyllabus']
        cid = dao.insertClass(cname, ccode, cdesc, term, years, cred, csyllabus)
        temp = (cid, cname, ccode, cdesc, term, years, cred, csyllabus)
        return jsonify(self.mapToDict(temp)), 201
    
    def updateClassById(self, cid, class_json):
        #Verify what atributtes are going to be updated
        dao = ClassDAO()
        cname = class_json['cname']
        ccode = class_json['ccode']
        cdesc = class_json['cdesc']
        term = class_json['term']
        years = class_json['years']
        cred = class_json['cred']
        csyllabus = class_json['csyllabus']
        if not "cname" or not "ccode" or not "cdesc" or not "term" or not "years" or not "cred" or not "csyllabus" in class_json:
            return jsonify(UpdateStatus = "Malformed post request"), 400
        temp = dao.updateClassById(cid, cname,ccode, cdesc, term, years, cred, csyllabus)
        if temp:
            tup = (cid, cname, ccode, cdesc, term, years, cred, csyllabus)
            return jsonify(self.mapToDict(tup)), 200
        else:
            return jsonify(UpdateStatus = "Class Not Found"), 404
    
    def deleteClassById(self, cid):
        dao = ClassDAO()
        temp = dao.deleteClassById(cid)
        if not temp:
            return jsonify(Error="Class Not Found"), 404
        else:
            return jsonify(DeleteStatus="OK"), 200
    
                               
                           
        
