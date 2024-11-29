import re
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
    
    def CountClassmapToDict(self, tuple):
        result = {}
        result["cid"] = tuple[0]
        result["cname"] = tuple[1]
        result["ccode"] = tuple[2]
        result["cdesc"] = tuple[3]
        result["term"] = tuple[4]
        result["years"] = tuple[5]
        result["cred"] = tuple[6]
        result["csyllabus"] = tuple[7]
        result["class_count"] = tuple[8]
        return result
    
    def MostPreReqmapToDict(self, tuple):
        result = {}
        result["cid"] = tuple[0]
        result["cname"] = tuple[1]
        result["ccode"] = tuple[2]
        result["cdesc"] = tuple[3]
        result["term"] = tuple[4]
        result["years"] = tuple[5]
        result["cred"] = tuple[6]
        result["csyllabus"] = tuple[7]
        result["prerequisite_classes"] = tuple[8]
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
        
    def getClassByCname_Ccode(self, cname, ccode):
        dao = ClassDAO()
        temp = dao.getClassByCname_Ccode(cname, ccode)
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
            if method == "update":
                return (
                    jsonify(UpdateStatus="cname DataType is incorrect must be str or char"),
                    400,
                )
            
            elif method == "insert":
                return (
                    jsonify(InsertStatus="cname DataType is incorrect must be str or char"),
                    400,
                )

        if not isinstance(ccode, str):
            if method == "update":
                return (
                    jsonify(UpdateStatus="ccode DataType is incorrect must be str or char"),
                    400,
                )
            
            elif method == "insert":
                return (
                    jsonify(InsertStatus="ccode DataType is incorrect must be str or char"),
                    400,
                )

        if not isinstance(cdesc, str):
            if method == "update":
                return (
                    jsonify(UpdateStatus="cdesc DataType is incorrect must be str or char"),
                    400,
                )
            
            elif method == "insert":
                return (
                    jsonify(InsertStatus="cdesc DataType is incorrect must be str or char"),
                    400,
                )

        if not isinstance(term, str):
            if method == "update":
                return (
                    jsonify(UpdateStatus="term DataType is incorrect must be str or char"),
                    400,
                )
            
            elif method == "insert":
                return (
                    jsonify(InsertStatus="term DataType is incorrect must be str or char"),
                    400,
                )

        if not isinstance(years, str):
            if method == "update":
                return (
                    jsonify(UpdateStatus="years DataType is incorrect must be str or char"),
                    400,
                )
            
            elif method == "insert":
                return (
                    jsonify(InsertStatus="years DataType is incorrect must be str or char"),
                    400,
                )

        if not isinstance(cred, int):
            if method == "update":
                return (
                    jsonify(UpdateStatus="cred DataType is incorrect must be int"),
                    400,
                )
            
            elif method == "insert":
                return (
                    jsonify(InsertStatus="cred DataType is incorrect must be int"),
                    400,
                )

        if not isinstance(csyllabus, str):
            if method == "update":
                return (
                    jsonify(UpdateStatus="csyllabus DataType is incorrect must be str or char"),
                    400,
                )
            
            elif method == "insert":
                return (
                    jsonify(InsertStatus="csyllabus DataType is incorrect must be str or char"),
                    400,
                )

        # Inspect Empty Entries
        if len(cname.strip()) == 0:
            if method == "update":
                return jsonify(UpdateStatus="cname is empty"), 400
            elif method == "insert":
                return jsonify(InsertStatus="cname is empty"), 400

        elif len(ccode.strip()) == 0:
            if method == "update":
                return jsonify(UpdateStatus="ccode is empty"), 400
            elif method == "insert":
                return jsonify(InsertStatus="ccode is empty"), 400

        elif len(cdesc.strip()) == 0:
            if method == "update":
                return jsonify(UpdateStatus="cdesc is empty"), 400
            elif method == "insert":
                return jsonify(InsertStatus="cdesc is empty"), 400

        elif len(term.strip()) == 0:
            if method == "update":
                return jsonify(UpdateStatus="term is empty"), 400
            elif method == "insert":
                return jsonify(InsertStatus="term is empty"), 400

        elif len(years.strip()) == 0:
            if method == "update":
                return jsonify(UpdateStatus="years is empty"), 400
            elif method == "insert":
                return jsonify(InsertStatus="years is empty"), 400

        elif len(csyllabus.strip()) == 0:
            if method == "update":
                return jsonify(UpdateStatus="csyllabus is empty"), 400
            elif method == "insert":
                return jsonify(InsertStatus="csyllabus is empty"), 400

        # Inspect correct lengths
        if len(cname) > 50:
            if method == "update":
                return jsonify(UpdateStatus="cname cannot exceed 50 characters"), 413
            elif method == "insert":
                return jsonify(InsertStatus="cname cannot exceed 50 characters"), 413

        if len(ccode) > 4:
            if method == "update":
                return jsonify(UpdateStatus="ccode cannot exceed 4 characters"), 413
            elif method == "insert":
                return jsonify(InsertStatus="ccode cannot exceed 4 characters"), 413

        if len(cdesc) > 100:
            if method == "update":
                return jsonify(UpdateStatus="cdesc cannot exceed 100 characters"), 413
            elif method == "insert":
                return jsonify(InsertStatus="cdesc cannot exceed 100 characters"), 413

        if len(term) > 35:
            if method == "update":
                return jsonify(UpdateStatus="term cannot exceed 35 characters"), 413
            elif method == "insert":
                return jsonify(InsertStatus="term cannot exceed 35 characters"), 413

        if len(years) > 20:
            if method == "update":
                return jsonify(UpdateStatus="years cannot exceed 20 characters"), 413
            elif method == "insert":
                return jsonify(InsertStatus="years cannot exceed 20 characters"), 413

        if len(csyllabus) > 255:
            if method == "update":
                return jsonify(UpdateStatus="csyllabus cannot exceed 255 characters"), 413
            elif method == "insert":
                return jsonify(InsertStatus="csyllabus cannot exceed 255 characters"), 413

        if cred > 9 or cred <= 0:
            if method == "update":
                return jsonify(UpdateStatus="Incorrect Credits Value"), 413
            elif method == "insert":
                return jsonify(InsertStatus="Incorrect Credits Value"), 413
        
        # Inspect Values for term and years
        if term not in ["First Semester", "Second Semester", "First Semester, Second Semester", "According to Demand", "V1", "V2"]:
            # Verify if the values were put without correct capital letters and if the values were put with white spaces
            if term.replace(" ", "").strip().lower() in ["firstsemester", "secondsemester", "firstsemester,secondsemester", "accordingtodemand", "v1", "v2"]:
                if term.replace(" ", "").strip().lower() == "firstsemester":
                    class_json['term'] = "First Semester"
                    temp['term'] = "First Semester"
                if term.replace(" ", "").strip().lower() == "secondsemester":
                    class_json['term'] = "Second Semester"
                    temp['term'] = "Second Semester"
                if term.replace(" ", "").strip().lower() == "firstsemester,secondsemester":
                    class_json['term'] = "First Semester, Second Semester"
                    temp['term'] = "First Semester, Second Semester"
                if term.replace(" ", "").strip().lower() == "accordingtodemand":
                    class_json['term'] = "According to Demand"
                    temp['term'] = "According to Demand"
                if term.replace(" ", "").strip().lower() == "v1":
                    class_json['term'] = "V1"
                    temp['term'] = "V1"
                if term.replace(" ", "").strip().lower() == "v2":
                    class_json['term'] = "V2"
                    temp['term'] = "V2"

            # Verify if the pair values were put without commas
            elif term.replace(" ", "").replace(",", "").strip().lower() == "firstsemestersecondsemester":
                class_json['term'] = "First Semester, Second Semester"
                temp['term'] = "First Semester, Second Semester"
                
            else: 
                if method == "update":
                    return jsonify(UpdateStatus="Incorrect term value, the options are: 'First Semester', 'Second Semester', 'First Semester, Second Semester', 'According to Demand', 'V1', 'V2'"), 400
                elif method == "insert":
                    return jsonify(InsertStatus="Incorrect term value, the options are: 'First Semester', 'Second Semester', 'First Semester, Second Semester', 'According to Demand'"), 400
        
        if years not in ["Even Years", "Odd Years", "According to Demand", "Every Year"]:
            # Verify if the values were put without correct capital letters and if the values were put with white spaces
            if years.replace(" ", "").strip().lower() in ["evenyears", "oddyears", "accordingtodemand", "everyyear"]:
                if (years.replace(" ", "").strip().lower() == "evenyears") or (years.replace(" ", "").strip().lower() == "evenyear"):
                    class_json['years'] = "Even Years"
                    temp['years'] = "Even Years"
                if (years.replace(" ", "").strip().lower() == "oddyears") or (years.replace(" ", "").strip().lower() == "oddyear"):
                    class_json['years'] = "Odd Years"
                    temp['years'] = "Odd Years"
                if (years.replace(" ", "").strip().lower() == "accordingtodemand") or (years.replace(" ", "").strip().lower() == "accordingtodemands"):
                    class_json['years'] = "According to Demand"
                    temp['years'] = "According to Demand"
                if (years.replace(" ", "").strip().lower() == "everyyear") or (years.replace(" ", "").strip().lower() == "everyyears"):
                    class_json['years'] = "Every Year"
                    temp['years'] = "Every Year"

            else:
                if method == "update":
                    return jsonify(UpdateStatus="Incorrect years value, the options are: 'Even Years', 'Odd Years', 'According to Demand', 'Every Year'"), 416
                elif method == "insert":
                    return jsonify(InsertStatus="Incorrect years value, the options are: 'Even Years', 'Odd Years', 'According to Demand', 'Every Year'"), 416
        
        # Inspect Duplicates before inserting or Updating (Dont use Primary Key, that is always diferent (serial))
        if method == "insert":
            cdescDuplicateCid = dao.cdescDuplicate(temp)
            csyllabusDuplicateCid = dao.csyllabusDuplicate(temp)
            cname_and_ccodeDuplicateCid = dao.cname_and_ccodeDuplicate(temp)

            if dao.exactDuplicate(temp, method):
                return jsonify(InsertStatus="Exact Duplicate Entry"), 400
            
            if cname_and_ccodeDuplicateCid is not None:
                return jsonify(InsertStatus="Duplicate entry: The class with 'cid' %s has the same 'Cname' %s and 'Ccode' %s. Delete or Update the existing class first." % (cname_and_ccodeDuplicateCid, temp["cname"], temp["ccode"])), 400
            
            if cdescDuplicateCid is not None:
                return jsonify(InsertStatus="Duplicate entry: The class with 'cid' %s has the same 'Cdesc' %s. Delete or Update the existing class first." % (cdescDuplicateCid, temp["cdesc"])), 400
            
            if csyllabusDuplicateCid is not None:
                return jsonify(InsertStatus="Duplicate entry: The class with 'cid' %s has the same 'Csyllabus' %s. Delete or Update the existing class first." % (csyllabusDuplicateCid, temp["csyllabus"])), 400
        
        elif method == "update":
            cdescDuplicateCid = dao.cdescDuplicate(temp)
            csyllabusDuplicateCid = dao.csyllabusDuplicate(temp)
            updateExactCid = dao.exactDuplicate(temp, method)
            cname_and_ccodeDuplicateCid = dao.cname_and_ccodeDuplicate(temp)

            if updateExactCid is not None:
                if updateExactCid != cid:
                    return jsonify(UpdateStatus="Duplicate Entry: The class with 'cid' %s has the same exact data" % updateExactCid), 400
                elif updateExactCid == cid:
                    return jsonify(UpdateStatus="Duplicate Entry: This class have the desired data, no changes made"), 400
                
            if cname_and_ccodeDuplicateCid is not None:
                if cname_and_ccodeDuplicateCid != cid:
                    return jsonify(UpdateStatus="Duplicate entry: The class with 'cid' %s has the same 'Cname' %s and 'Ccode' %s. Delete or Update the existing class first." % (cname_and_ccodeDuplicateCid, temp["cname"], temp["ccode"])), 400
            
            if cdescDuplicateCid is not None:
                if cdescDuplicateCid != cid:
                    return jsonify(UpdateStatus="Duplicate entry: The class with 'cid' %s has the same 'Cdesc' %s. Delete or Update the existing class first." % (cdescDuplicateCid, temp["cdesc"])), 400
                 
            if csyllabusDuplicateCid is not None:
                if csyllabusDuplicateCid != cid:
                    return jsonify(UpdateStatus="Duplicate entry: The class with 'cid' %s has the same 'Csyllabus' %s. Delete or Update the existing class first." % (csyllabusDuplicateCid, temp["csyllabus"])), 400

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
        original_SectionSize = sections_df.shape[0]
        if not dao.classExists(cid):
            return jsonify(UpdateStatus="Class Not Found"), 404
        
        result_class_df = rem_courses_with_invalid_timeframe(sections_df, class_df)

        if (result_class_df[0].shape[0] != original_SectionSize) and (original_SectionSize != 0 and original_SectionSize != None):

            return (
                jsonify(
                    UpdateStatus=("This class have associated sections, and not all complish the new term or years values. First modify the sections."
                    )
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

        if temp:
            for row in temp:
                result.append(self.MostPreReqmapToDict(row))
            return jsonify(result)
        else:
            return jsonify(Error="Not Found"), 404

    def getMostPerRoom(self, id):
        result = []
        dao = ClassDAO()
        temp = dao.getMostPerRoom(id)
        
        if temp:
            for row in temp:
                result.append(self.CountClassmapToDict(row))
            return jsonify(result)
        else:
            return jsonify(Error="Not Found"), 404

    def getLeastClass(self):
        result = []
        dao = ClassDAO()
        temp = dao.getLeastClass()

        if temp:
            for row in temp:
                result.append(self.CountClassmapToDict(row))
            return jsonify(result)
        else:
            return jsonify(Error="Not Found"), 404

    def getMostPerSemester(self, year, semester):
        result = []
        dao = ClassDAO()
        temp = dao.getMostPerSemester(year, semester)

        if temp:
            for row in temp:
                result.append(self.CountClassmapToDict(row))
            return jsonify(result)
        else:
            return jsonify(Error="Not Found"), 404
