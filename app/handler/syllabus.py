from flask import jsonify
from dao.syllabus import SyllabusDAO

class SyllabusHandler:
    def mapToDict(self, tuple):
        result = {}
        result["chunkid"] = tuple[0]
        result["courseid"] = tuple[1]
        result["embedding_text"] = tuple[2]
        result["chunk"] = tuple[3]
        return result
    
    def getAllSyllabus(self):
        result = []
        dao = SyllabusDAO()
        temp = dao.getAllSyllabus()
        
        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)
    
    def getSyllabusByCid(self, cid):
        dao = SyllabusDAO()
        result = dao.getAllSyllabusByCid(cid)
        return jsonify(result)
    
    def insertSyllabus(self, syllabus_json):
        if (
            "courseid" not in syllabus_json
            or "embedding_text" not in syllabus_json
            or "chunk" not in syllabus_json
        ):
            return jsonify(InsertStatus="Missing required fields"), 400
        
        courseid = syllabus_json["courseid"]
        embedding_text = syllabus_json["embedding_text"]
        chunk = syllabus_json["chunk"]
        
        if not isinstance(courseid, int):
            return jsonify(InsertStatus="Invalid datatype for courseid"), 400
        
        dao = SyllabusDAO()
        chunkid = dao.insertSyllabus(courseid, embedding_text, chunk)
        
        return jsonify(InsertStatus="Success", chunkid=chunkid), 201
    
    
    
    