from flask import Flask, jsonify, request
from flask_cors import CORS
import os


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


@app.route("/segmentation_fault/class", methods=["GET", "POST"])
def courses():
    if request.method == "GET":
        return ClassHandler().getAllClass()
    elif request.method == "POST":
        return ClassHandler().insertClass(request.json)
    
@app.route("/segmentation_fault/class/<int:cid>", methods=["GET", "PUT", "DELETE"])
def courses2(cid):
    if request.method == "GET":
        return ClassHandler().getclassById(cid)
    elif request.method == "PUT":
        return ClassHandler().updateClassById(cid, request.json)
    elif request.method == "DELETE":
        return ClassHandler().deleteClassById(cid)

@app.route("/segmentation_fault/requisite")
def requisite():
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


