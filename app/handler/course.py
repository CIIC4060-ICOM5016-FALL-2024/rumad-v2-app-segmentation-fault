from flask import jsonify
from dao.course import ClassDAO
import pandas as pd
from handler.data_validation import rem_courses_with_invalid_timeframe


class ClassHandler:
    def mapToDict(self, tuple):
        result = {}
        result["cid"] = tuple[0]
        result["cname"] = tuple[1]
        result["ccode"] = tuple[2]
        result["cdesc"] = tuple[3]
        result["term"] = tuple[4]
        result["years"] = tuple[5]
        result["cred"] = tuple[6]
        result["csyllabus"] = tuple[7]
        return result

    def getAllClass(self):
        result = []
        dao = ClassDAO()
        temp = dao.getAllClass()

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)

    def getclassById(self, cid):
        dao = ClassDAO()
        temp = dao.getClassById(cid)
        if not temp:
            return jsonify(Error="Class Not Found"), 404
        else:
            result = self.mapToDict(temp)
            return jsonify(result)

    def inspectInputData(self, class_json, method, cid):
        dao = ClassDAO()
        # Inspect if all keys are present
        if not all(
            key in class_json
            for key in ["cname", "ccode", "cdesc", "term", "years", "cred", "csyllabus"]
        ):
            return jsonify(InsertStatus="Malformed post request"), 400

        cname = class_json["cname"]
        ccode = class_json["ccode"]
        cdesc = class_json["cdesc"]
        term = class_json["term"]
        years = class_json["years"]
        cred = class_json["cred"]
        csyllabus = class_json["csyllabus"]

        temp = {
            "cname": cname,
            "ccode": ccode,
            "cdesc": cdesc,
            "term": term,
            "years": years,
            "cred": cred,
            "csyllabus": csyllabus,
        }

        # Inspect Incorrect DataTypes
        if not isinstance(cname, str):
            return (
                jsonify(UpdateStatus="cname DataType is incorrect must be str or char"),
                400,
            )

        if not isinstance(ccode, str):
            return (
                jsonify(UpdateStatus="ccode DataType is incorrect must be str or char"),
                400,
            )

        if not isinstance(cdesc, str):
            return (
                jsonify(UpdateStatus="cdesc DataType is incorrect must be str or char"),
                400,
            )

        if not isinstance(term, str):
            return (
                jsonify(UpdateStatus="term DataType is incorrect must be str or char"),
                400,
            )

        if not isinstance(years, str):
            return (
                jsonify(UpdateStatus="years DataType is incorrect must be str or char"),
                400,
            )

        if not isinstance(cred, int):
            return (
                jsonify(UpdateStatus="cred DataType is incorrect must be Integer"),
                400,
            )

        if not isinstance(csyllabus, str):
            return (
                jsonify(
                    UpdateStatus="csyllabus DataType is incorrect must be str or char"
                ),
                400,
            )

        # Inspect Empty Entries
        if len(cname.strip()) == 0:
            return jsonify(UpdateStatus="cname is empty"), 400

        elif len(ccode.strip()) == 0:
            return jsonify(UpdateStatus="ccode is empty"), 400

        elif len(cdesc.strip()) == 0:
            return jsonify(UpdateStatus="cdesc is empty"), 400

        elif len(term.strip()) == 0:
            return jsonify(UpdateStatus="term is empty"), 400

        elif len(years.strip()) == 0:
            return jsonify(UpdateStatus="years is empty"), 400

        elif len(csyllabus.strip()) == 0:
            return jsonify(UpdateStatus="csyllabus is empty"), 400

        # Inspect correct lengths
        if len(cname) > 50:
            return jsonify(UpdateStatus="cname cannot exceed 50 characters"), 400

        if len(ccode) > 4:
            return jsonify(UpdateStatus="ccode cannot exceed 4 characters"), 400

        if len(cdesc) > 100:
            return jsonify(UpdateStatus="cdesc cannot exceed 4 characters"), 400

        if len(term) > 35:
            return jsonify(UpdateStatus="term cannot exceed 4 characters"), 400

        if len(years) > 20:
            return jsonify(UpdateStatus="years cannot exceed 20 characters"), 400

        if len(csyllabus) > 255:
            return jsonify(UpdateStatus="csyllabus cannot exceed 255 characters"), 400

        if cred > 9 or cred <= 0:
            return jsonify(UpdateStatus="Incorrect Credits Value"), 400
        
        # Inspect Duplicates before inserting or Updating (Dont use Primary Key, that is always diferent (serial))
        if method == "insert":
            if dao.exactDuplicate(temp, method):
                return jsonify(InsertStatus="Exact Duplicate Entry"), 400
            
            insertCcodeDuplicateCid = dao.insertCcodeDuplicate(temp)
            if insertCcodeDuplicateCid is not None:
                return jsonify(InsertStatus="Duplicate entry: The class with 'cid' %s has the same 'Ccode' %s. Delete or Update the existing class first." % (insertCcodeDuplicateCid, temp["ccode"])), 400
            
            insertCdescDuplicateCid = dao.insertCdescDuplicate(temp)
            if insertCdescDuplicateCid is not None:
                return jsonify(InsertStatus="Duplicate entry: The class with 'cid' %s has the same 'Cdesc' %s. Delete or Update the existing class first." % (insertCdescDuplicateCid, temp["cdesc"])), 400
            
            insertCsyllabusDuplicateCid = dao.insertCsyllabusDuplicate(temp)
            if insertCsyllabusDuplicateCid is not None:
                return jsonify(InsertStatus="Duplicate entry: The class with 'cid' %s has the same 'Csyllabus' %s. Delete or Update the existing class first." % (insertCsyllabusDuplicateCid, temp["csyllabus"])), 400
        
        elif method == "update":
            insertCcodeDuplicateCid = dao.insertCcodeDuplicate(temp)
            insertCdescDuplicateCid = dao.insertCdescDuplicate(temp)
            insertCsyllabusDuplicateCid = dao.insertCsyllabusDuplicate(temp)
            updateExactCid = dao.exactDuplicate(temp, method)

            if updateExactCid is not None:
                return jsonify(UpdateStatus="Duplicate Entry: The class with 'cid' %s has the same exact data" % updateExactCid), 400
            
            if insertCcodeDuplicateCid is not None:
                if insertCcodeDuplicateCid != cid:
                    return jsonify(UpdateStatus="Duplicate entry: The class with 'cid' %s has the same 'Ccode' %s. Delete or Update the existing class first." % (insertCcodeDuplicateCid, temp["ccode"])), 400
                    
            if insertCdescDuplicateCid is not None:
                if insertCdescDuplicateCid != cid:
                    return jsonify(UpdateStatus="Duplicate entry: The class with 'cid' %s has the same 'Cdesc' %s. Delete or Update the existing class first." % (insertCdescDuplicateCid, temp["cdesc"])), 400
                 
            if insertCsyllabusDuplicateCid is not None:
                if insertCsyllabusDuplicateCid != cid:
                    return jsonify(UpdateStatus="Duplicate entry: The class with 'cid' %s has the same 'Csyllabus' %s. Delete or Update the existing class first." % (insertCsyllabusDuplicateCid, temp["csyllabus"])), 400

    def insertClass(self, class_json):
        returnStatement = self.inspectInputData(class_json, "insert", None)
        if returnStatement is not None:
            return returnStatement

        dao = ClassDAO()
        cname = class_json["cname"]
        ccode = class_json["ccode"]
        cdesc = class_json["cdesc"]
        term = class_json["term"]
        years = class_json["years"]
        cred = class_json["cred"]
        csyllabus = class_json["csyllabus"]
     
        cid = dao.insertClass(cname, ccode, cdesc, term, years, cred, csyllabus)
        result = (cid, cname, ccode, cdesc, term, years, cred, csyllabus)
        return jsonify(self.mapToDict(result)), 201

    def updateClassById(self, cid, class_json):
        returnStatement = self.inspectInputData(class_json, "update", cid)
        if returnStatement is not None:
            return returnStatement

        dao = ClassDAO()
        cname = class_json["cname"]
        ccode = class_json["ccode"]
        cdesc = class_json["cdesc"]
        term = class_json["term"]
        years = class_json["years"]
        cred = class_json["cred"]
        csyllabus = class_json["csyllabus"]

        # Verify Phase 1 Constrains
        # ------------------------------------------------------------------------
        # Verify if class to update have a asociate section
        tempClass = {
            "cid": cid,
            "cname": cname,
            "ccode": ccode,
            "cdesc": cdesc,
            "term": term,
            "years": years,
            "cred": cred,
            "csyllabus": csyllabus,
        }
        class_df = pd.DataFrame([tempClass])
        sections_df = dao.verifySectionsAs(cid)
        result_class_df = rem_courses_with_invalid_timeframe(sections_df, class_df)

        if not dao.classExists(cid):
            return jsonify(UpdateStatus="Class Not Found"), 404

        if result_class_df[0].empty and not sections_df.empty:
            return (
                jsonify(
                    UpdateStatus="It is not possible to modify the term or year for classes that have associated sections, First modify the sections"
                ),
                400,
            )
        # ------------------------------------------------------------------------

        temp = dao.updateClassById(
            cid, cname, ccode, cdesc, term, years, cred, csyllabus
        )
        if temp:
            tup = (cid, cname, ccode, cdesc, term, years, cred, csyllabus)
            return jsonify(self.mapToDict(tup)), 200
        else:
            return jsonify(UpdateStatus="Class Not Found"), 404

    def deleteClassById(self, cid):
        dao = ClassDAO()
        temp = dao.deleteClassById(cid)
        if not temp:
            return jsonify(DeleteStatus="Class Not Found"), 404
        else:
            return jsonify(DeleteStatus="OK"), 200

    def getMostPrerequisite(self):
        result = []
        dao = ClassDAO()
        temp = dao.getMostPrerequisite()

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)

    def getMostPerRoom(self, id):
        result = []
        dao = ClassDAO()
        temp = dao.getMostPerRoom(id)

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)

    def getLeastClass(self):
        result = []
        dao = ClassDAO()
        temp = dao.getLeastClass()

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)

    def getMostPerSemester(self, year, semester):
        result = []
        dao = ClassDAO()
        temp = dao.getMostPerSemester(year, semester)

        for row in temp:
            result.append(self.mapToDict(row))
        return jsonify(result)
