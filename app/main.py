from flask import Flask, jsonify, request
from flask_cors import CORS

from handler.section import SectionHandler
from handler.course import ClassHandler

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


@app.route("/segmentation_fault/class", methods=["GET", "POST", "PUT", "DELETE"])
def courses():
    if request.method == "GET":
        return ClassHandler().getAllClass()
    elif request.method == "POST":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    
@app.route("/segmentation_fault/requisite")
def requisite():
    pass


if __name__ == "__main__":
    app.run(debug=True)
