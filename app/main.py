from flask import Flask, jsonify, request
from flask_cors import CORS

from handler.room import RoomHandler
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
    return RoomHandler().getAllRoom()


@app.route("/segmentation_fault/class")
def courses():
    pass


@app.route("/segmentation_fault/requisite")
def requisite():
    pass


if __name__ == "__main__":
    app.run(debug=True)
