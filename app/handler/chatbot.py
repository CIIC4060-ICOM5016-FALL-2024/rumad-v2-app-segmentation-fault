import requests
import re

from flask import jsonify
from dao.syllabus import SyllabusDAO
from dao.course import ClassDAO

url = "https://c2d9-24-55-160-197.ngrok-free.app/segmentation_fault/"


class ChatbotHandler:
    def getResponse(self, context_json):
        if not context_json or "question" not in context_json:
            return jsonify(UpdateStatus="Missing required fields"), 400
        
        if not isinstance(context_json["question"], str):
            return jsonify(UpdateStatus="Invalid context type"), 400
                
        context = ""
        if "context" in context_json:
            if not isinstance(context_json["context"], str):
                return jsonify(UpdateStatus="Invalid context type"), 400
            context = context_json["context"]            
        question = context_json["question"]

        class_dao = ClassDAO()
        expected_cnames = ["CIIC", "INSO"]
        pattern = rf"({'|'.join(expected_cnames)})[\s]*(\d+)"
        matches = re.findall(pattern, question, flags=re.IGNORECASE)
        expected_course_ids = None
        expected_course_id = None
        result = []
        for match in matches:
            result.append({"cname": match[0].upper(), "ccode": match[1]})

        if result and len(result) > 1:
            expected_course_ids = []
            for r in result:
                expected_course_ids.append(
                    class_dao.getClassByCname_Ccode(r["cname"].upper(), r["ccode"])[0]
                )

        elif result:
            expected_course_id = class_dao.getClassByCname_Ccode(
                result[0]["cname"].upper(), result[0]["ccode"]
            )[0]

        question_embedding_str = ""
        try:
            question_embedding = requests.post(url + "embedding", json={"text": question})
            question_embedding_str = question_embedding.json()["embedding"]

        except Exception as e:
            return jsonify(UpdateStatus=f"Internal error: {str(e)}"), 500
        
        dao = SyllabusDAO()
        fragments = []
        if expected_course_id:
            fragments = dao.getAllFragments(question_embedding_str, expected_course_id)

        elif expected_course_ids:
            fragments = dao.getAllFragments3(question_embedding_str, expected_course_ids)
        else:
            fragments = dao.getAllFragments2(question_embedding_str)

        documents = "\n".join(fragment[2] for fragment in fragments)

        context = context + "\nDocuments: '" + documents + "'"

        response = None
        try:
            response = requests.post(url + "ollama", json={"context": context, "question": question})
        except Exception as e:
            return jsonify(UpdateStatus=f"Internal error: {str(e)}"), 500
        
        return response.json()