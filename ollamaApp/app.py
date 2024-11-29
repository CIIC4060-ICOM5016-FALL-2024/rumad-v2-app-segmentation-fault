from flask import Flask, request, jsonify
from flask_cors import CORS
from handler.ollama_chat import OllamaChatHandler

app = Flask(__name__)
CORS(app)

@app.route("/")
def ollama_app():
    return "Ollama chat for main page"

@app.route("/segmentation_fault/ollama", methods=["POST"])
def get_response():
    return OllamaChatHandler().getResponse(request.json)

@app.route("/segmentation_fault/embedding", methods=["POST"])
def get_embedding():
    return OllamaChatHandler().getEmbedding(request.json)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)