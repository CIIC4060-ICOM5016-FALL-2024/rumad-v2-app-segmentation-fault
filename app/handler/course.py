from calendar import c
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

        # Verify if all keys are present
        if not all(key in class_json for key in ["cname", "ccode", "cdesc", "term", "years", "cred", "csyllabus"]):
            return jsonify(InsertStatus="Malformed post request"), 400
        
        cname = class_json['cname']
        ccode = class_json['ccode']
        cdesc = class_json['cdesc']
        term = class_json['term']
        years = class_json['years']
        cred = class_json['cred']
        csyllabus = class_json['csyllabus']

        # Verify if cred value are of the correct length
        if len(cred) > 1:
            return jsonify(UpdateStatus = "Incorrect Credits Value"), 400

        # Verify if all values are of the correct type
        if not all(isinstance(class_json[key], str) for key in ["cname", "ccode", "cdesc", "term", "years", "csyllabus"] or isinstance(class_json['cred'], int)):
            return jsonify(UpdateStatus = "Incorrect Datatype, verify entries"), 400
        
        temp = {"cname": cname, "ccode": ccode, "cdesc": cdesc, "term": term, "years": years, "cred": cred, "csyllabus": csyllabus}
        
        # Verify Duplicates before inserting (Dont use Primary Key, that is always diferent (serial))
        if dao.exactDuplicate(temp):
            return jsonify(UpdatetStatus = "Duplicate Entry"), 400
        
        cid = dao.insertClass(cname, ccode, cdesc, term, years, cred, csyllabus)
        result = (cid, cname, ccode, cdesc, term, years, cred, csyllabus)
        return jsonify(self.mapToDict(result)), 201
    
    def updateClassById(self, cid, class_json):
        dao = ClassDAO()

        if not all(key in class_json for key in ["cname", "ccode", "cdesc", "term", "years", "cred", "csyllabus"]):
            return jsonify(InsertStatus="Malformed post request"), 400
            
        cname = class_json['cname']
        ccode = class_json['ccode']
        cdesc = class_json['cdesc']
        term = class_json['term']
        years = class_json['years']
        cred = class_json['cred']
        csyllabus = class_json['csyllabus']

        # Verify str length of all values
        if any(len(value.strip()) == 0 for value in [cname, ccode, cdesc, term, years, csyllabus]):
            return jsonify(UpdateStatus="A entry is empty"), 400


        # Verify if cred value are of the correct length
        if cred > 9 or cred <= 0:
            return jsonify(UpdateStatus = "Incorrect Credits Value"), 400
        
        # Verify if all values are of the correct type
        if not all(isinstance(class_json[key], str) for key in ["cname", "ccode", "cdesc", "term", "years", "csyllabus"] or isinstance(class_json['cred'], int)):
            return jsonify(UpdateStatus = "Incorrect Datatype, verify entries"), 400

        tempV = {"cname": cname, "ccode": ccode, "cdesc": cdesc, "term": term, "years": years, "cred": cred, "csyllabus": csyllabus}

        # Verify Duplicates before inserting (Dont use Primary Key, that is always diferent (serial))
        if dao.exactDuplicate(tempV):
            return jsonify(InsertStatus = "Duplicate Entry"), 400
        
        elif dao.credDuplicate(tempV):
            return jsonify(UpdateStatus = "Duplicate Entry"), 400
        
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
            return jsonify(DeleteStatus = "Class Not Found"), 404
        else:
            return jsonify(DeleteStatus = "OK"), 200
        
    def getMostPrerequisite(self):
        result = []
        dao = ClassDAO()
        temp = dao.getMostPrerequisite()
        
        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)
    
    def getMostPerRoom(self, id):
        result = []
        dao = ClassDAO()
        temp = dao.getMostPerRoom(id)
        
        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)
    
    def getLeastClass(self):
        result = []
        dao = ClassDAO()
        temp = dao.getLeastClass()
        
        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)


    def getMostPerSemester(self, year, semester):
        result = []
        dao = ClassDAO()
        temp = dao.getMostPerSemester(year, semester)
        
        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)

                           
        
