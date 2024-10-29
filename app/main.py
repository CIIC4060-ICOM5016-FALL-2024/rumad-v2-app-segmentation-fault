from flask import Flask, jsonify, request
from flask_cors import CORS
import os


from handler.section import SectionHandler

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/segmentation_fault/section")
def section():
    return SectionHandler().getAllSection()


@app.route("/segmentation_fault/meeting")
def meeting():
    pass


@app.route("/segmentation_fault/room")
def room():
    pass


@app.route("/segmentation_fault/class")
def courses():
    pass


@app.route("/segmentation_fault/requisite")
def requisite():
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
