from flask import jsonify
from dao.syllabus import SyllabusDAO
import requests

url = "https://7044-24-55-160-197.ngrok-free.app/segmentation_fault/"


class ChatbotHandler:
    def getResponse(self, context_json):
        if not context_json or "context" not in context_json:
            return jsonify(UpdateStatus="Missing required fields"), 400
        
        if not isinstance(context_json["context"], str):
            return jsonify(UpdateStatus="Invalid context type"), 400
        
        context = context_json["context"]
        context_embedding_str = ""
        try:
            context_embedding = requests.post(url + "embedding", json={"text": context})
            context_embedding_str = context_embedding.json()["embedding"]

        except Exception as e:
            return jsonify(UpdateStatus=f"Internal error: {str(e)}"), 500
        

        dao = SyllabusDAO()
        fragments = dao.getAllFragments2(context_embedding_str)
        documents = "\n".join(fragment[2] for fragment in fragments)

        response = None
        try:
            response = requests.post(url + "ollama", json={"context": documents, "question": context})
        except Exception as e:
            return jsonify(UpdateStatus=f"Internal error: {str(e)}"), 500
        
        return response.json()