from flask import jsonify
import sys
import os
import json

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

class ChatbotHandler:
    def getAnswer(self, question_json):
        if not question_json:
            return jsonify(Error="Question is required"), 400

        # Import the chatbot within the method
        from vectorDB.chatBot.chat import chatbot

        try:
            response_json = chatbot(question_json)
            response_dict = json.loads(response_json)
        except json.JSONDecodeError as e:
            # Handle JSON format errors
            return jsonify(Error="Invalid JSON format return", Details=str(e)), 400
        except ConnectionError as e:
            # Handle connection errors
            return jsonify(Error="Connection error", Details=str(e)), 503
        except Exception as e:
            # Handle other unexpected errors
            return jsonify(Error="An unexpected error occurred", Details=str(e)), 500

        # Return the response as a JSON
        return jsonify(response_dict), 200