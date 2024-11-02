from flask import Flask, jsonify, request
from flask_cors import CORS


from handler.section import SectionHandler
from handler.meeting import MeetingHandler
from handler.requisite import RequisiteHandler

app = Flask(__name__)
CORS(app)


# ROOT ROUTE
@app.route("/")
def hello_world():
    return "This is the RestAPI of Segmentation Fault team."


# SECTION ROUTES
@app.route("/segmentation_fault/section", methods=["GET", "POST"])
def section():
    if request.method == "GET":
        return SectionHandler().getAllSection()
    else:
        return "POST"


@app.route("/segmentation_fault/section/<int:sid>", methods=["GET", "PUT", "DELETE"])
def sectionByID(sid):
    if request.method == "DELETE":
        return SectionHandler().deleteSectionBySid(sid)
    elif request.method == "PUT":
        return "PUT"
    else:
        return SectionHandler().getSectionBySid(sid)


# MEETING ROUTES
@app.route("/segmentation_fault/meeting")
def meeting():
    return MeetingHandler().getAllMeeting()


@app.route("/segmentation_fault/meeting/<int:mid>")
def getMeetingByMid(mid):
    return MeetingHandler().getMeetingByMid(mid)


# ROOM ROUTES
@app.route("/segmentation_fault/room")  # type: ignore
def room():
    pass


# CLASS ROUTES
@app.route("/segmentation_fault/class")  # type: ignore
def courses():
    pass


# REQUISITE ROUTES
@app.route("/segmentation_fault/requisite")
def requisite():
    return RequisiteHandler().getAllRequisite()


@app.route("/segmentation_fault/requisite/<int:classid>/<int:reqid>")
def getRequisiteByClassIdReqId(classid, reqid):
    return RequisiteHandler().getRequisiteByClassIdReqId(classid, reqid)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
