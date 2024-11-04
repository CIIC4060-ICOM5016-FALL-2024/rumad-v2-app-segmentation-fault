from flask import Flask, request
from flask_cors import CORS

from handler.section import SectionHandler
from handler.meeting import MeetingHandler
from handler.requisite import RequisiteHandler
from handler.course import ClassHandler
from handler.room import RoomHandler

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
        return SectionHandler().insertSection(request.json)


@app.route("/segmentation_fault/section/<int:sid>", methods=["GET", "PUT", "DELETE"])
def sectionByID(sid):
    if request.method == "DELETE":
        return SectionHandler().deleteSectionBySid(sid)
    elif request.method == "PUT":
        return SectionHandler().updateSectionBySid(sid, request.json)
    else:
        return SectionHandler().getSectionBySid(sid)


# MEETING ROUTES
@app.route("/segmentation_fault/meeting", methods=["GET", "POST"])
def meeting():
    if request.method == "GET":
        return MeetingHandler().getAllMeeting()
    else:
        return MeetingHandler().insertMeeting(request.json)


@app.route("/segmentation_fault/meeting/<int:mid>", methods=["GET", "PUT", "DELETE"])
def meetingByMID(mid):
    if request.method == "GET":
        return MeetingHandler().getMeetingByMid(mid)
    elif request.method == "PUT":
        return MeetingHandler().updateMeetingByMid(mid, request.json)
    else:
        return MeetingHandler().deleteMeetingByMid(mid)


# ROOM ROUTES
@app.route("/segmentation_fault/room", methods=["GET", "POST"])
def room():
    if request.method == "GET":
        return RoomHandler().getAllRoom()
    else:
        return RoomHandler().insertRoom(request.json)


@app.route("/segmentation_fault/room/<int:rid>", methods=["GET", "PUT", "DELETE"])
def roomByRID(rid):
    if request.method == "GET":
        return RoomHandler().getRoomByRid(rid)
    elif request.method == "PUT":
        return RoomHandler().updateRoomByRid(rid, request.json)
    else:
        return RoomHandler().deleteRoomByRid(rid)

# CLASS ROUTES
@app.route("/segmentation_fault/class", methods=["GET", "POST"])
def courses():
    if request.method == "GET":
        return ClassHandler().getAllClass()
    elif request.method == "POST":
        return ClassHandler().insertClass(request.json)


@app.route("/segmentation_fault/class/<int:cid>", methods=["GET", "PUT", "DELETE"])
def courseByID(cid):
    if request.method == "GET":
        return ClassHandler().getclassById(cid)
    elif request.method == "PUT":
        return ClassHandler().updateClassById(cid, request.json)
    elif request.method == "DELETE":
        return ClassHandler().deleteClassById(cid)


# REQUISITE ROUTES
@app.route("/segmentation_fault/requisite", methods=["GET", "POST"])
def requisite():
    if request.method == "GET":
        return RequisiteHandler().getAllRequisite()
    else:
        return RequisiteHandler().insertRequisite(request.json)


@app.route(
    "/segmentation_fault/requisite/<int:classid>/<int:reqid>",
    methods=["GET", "PUT", "DELETE"],
)
def requisiteByClassIdReqId(classid, reqid):
    if request.method == "DELETE":
        return RequisiteHandler().deleteRequisiteByClassIdReqId(classid, reqid)
    elif request.method == "PUT":
        return RequisiteHandler().updateRequisiteByClassIdReqId(
            classid, reqid, request.json
        )
    else:
        return RequisiteHandler().getRequisiteByClassIdReqId(classid, reqid)


# LOCAL STATICS (0/4)
# Top 3 rooms per building with the most capacity
@app.route("/segmentation_fault/<string:building>/capacity", methods=['GET'])
def getMaxCapacity(building):
    return RoomHandler().getMaxCapacity(building)

@app.route("/segmentation_fault/room/<string:building>/ratio", methods=['GET'])
def getRatioByBuilding(building):
    #TODO: Ask what supposed to be the input
    return RoomHandler().getRatioByBuilding(building)

# Top 3 classes that were taught the most per room
@app.route("/segmentation_fault/room/<cid>/classes", methods=["GET"])
def mostPerRoom(cid):
    return ClassHandler().getMostPerRoom(cid)


# GLOBAL STATICS (2/4)
# Top 5 meetings with the most sections
@app.route("/segmentation_fault/most/meeting", methods=["GET"])
def mostMeeting():
    return MeetingHandler().getMostMeeting()


# Top 3 classes that appears the most as prerequisite to other classes
@app.route("/segmentation_fault/most/prerequisite", methods=["GET"])
def mostPrerequisite():
    return ClassHandler().getMostPrerequisite()


# Total number of sections per year
@app.route("/segmentation_fault/section/year", methods=["GET"])
def sectionYear():
    return SectionHandler().getSectionPerYear()


if __name__ == "__main__":
    app.run(debug=True, port=8080)
