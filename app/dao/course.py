from config.db_config import pg_config
import pandas as pd
import psycopg2 as pg


class ClassDAO:
    def __init__(self):
        # Create the connection string
        url = "dbname=%s password=%s user=%s host=%s port=%s" % (
            pg_config["dbname"],
            pg_config["password"],
            pg_config["user"],
            pg_config["host"],
            pg_config["port"],
        )

        self.conn = pg.connect(url)

    def getAllClass(self):
        cursor = self.conn.cursor()
        query = (
            "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class;"
        )
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getClassById(self, cid):
        cursor = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class WHERE cid = %s;"
        cursor.execute(query, [cid])
        result = cursor.fetchone()
        return result

    def exactDuplicate(self, Val, method):
        cursor = self.conn.cursor()
        find_duplicate_query = "SELECT * FROM class WHERE cname = %s AND ccode = %s AND cdesc = %s AND term = %s AND years = %s AND cred = %s AND csyllabus = %s;"
        cursor.execute(
            find_duplicate_query,
            (
                Val["cname"],
                Val["ccode"],
                Val["cdesc"],
                Val["term"],
                Val["years"],
                Val["cred"],
                Val["csyllabus"],
            ),
        )
        if method == "insert":
            return cursor.rowcount == 1
        
        elif method == "update":
             result = cursor.fetchone()
             if result is not None:
                return result[0]
             return None
    
    
    def cname_and_ccodeDuplicate(self, tempV):
        cursor = self.conn.cursor()
        find_duplicate_query = "SELECT cid FROM class WHERE cname = %s AND ccode = %s;"
        cursor.execute(find_duplicate_query, (tempV["cname"], tempV["ccode"]))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return None
    
    
    def cdescDuplicate(self, tempV):
        cursor = self.conn.cursor()
        find_duplicate_query = "SELECT cid FROM class WHERE cdesc = %s;"
        cursor.execute(find_duplicate_query, (tempV["cdesc"],))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return None
    
    def csyllabusDuplicate(self, tempV):
        cursor = self.conn.cursor()
        find_duplicate_query = "SELECT cid FROM class WHERE csyllabus = %s;"
        cursor.execute(find_duplicate_query, (tempV["csyllabus"],))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return None
    
    def classExists(self, cid):
        cursor = self.conn.cursor()
        query = "SELECT * FROM class WHERE cid = %s;"
        cursor.execute(query, [cid])
        return cursor.rowcount == 1
    
    def verifySectionsAs(self, cid):
        cursor = self.conn.cursor()
        query = "SELECT * FROM section WHERE cid = %s;"
        cursor.execute(query, [cid])
        result = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns)
        
        return df

    def insertClass(self, cname, ccode, cdesc, term, years, cred, csyllabus):
        cursor = self.conn.cursor()
        query = "INSERT INTO class(cname, ccode, cdesc, term, years, cred, csyllabus) VALUES (%s, %s, %s, %s, %s, %s, %s) returning cid;"
        cursor.execute(query, [cname, ccode, cdesc, term, years, cred, csyllabus])
        cid = cursor.fetchone()[0]  # type: ignore
        self.conn.commit()
        return cid

    def updateClassById(self, cid, cname, ccode, cdesc, term, years, cred, csyllabus):
        cursor = self.conn.cursor()
        query = "UPDATE class SET cname = %s, ccode = %s, cdesc = %s, term = %s, years = %s, cred = %s, csyllabus = %s WHERE cid = %s;"
        cursor.execute(query, [cname, ccode, cdesc, term, years, cred, csyllabus, cid])
        self.conn.commit()
        # return boolean if the update was successful
        rowcount = cursor.rowcount
        return rowcount == 1

    def deleteClassById(self, cid):

        # Verify in the tables that have a foreign key to class first to avoid reference errors
        # -------------------------------------------------------------------------------------
        cursor = self.conn.cursor()
        find_sec = "SELECT * FROM section WHERE cid = %s;"
        find_req = "SELECT * FROM requisite WHERE classid = %s;"
        find_syllabus = "SELECT * FROM syllabus WHERE courseid = %s;"
        cursor.execute(find_sec, [cid])

        if cursor.rowcount > 0:
            section_q = "DELETE FROM section WHERE cid = %s;"
            cursor.execute(section_q, [cid])
            self.conn.commit()

        cursor.execute(find_req, [cid])

        if cursor.rowcount > 0:
            req_q = "DELETE FROM requisite WHERE classid = %s;"
            cursor.execute(req_q, [cid])
            self.conn.commit()

        cursor.execute(find_syllabus, [cid])

        if cursor.rowcount > 0:
            syllabus_q = "DELETE FROM syllabus WHERE courseid = %s;"
            cursor.execute(syllabus_q, [cid])
            self.conn.commit()
        # -------------------------------------------------------------------------------------
        # Then delete the class
        query = "DELETE FROM class WHERE cid = %s;"
        cursor.execute(query, [cid])
        self.conn.commit()
        rowcount = cursor.rowcount
        return rowcount == 1

    def getMostPrerequisite(self):
        cursor = self.conn.cursor()
        query = "SELECT c.cid, c.cname, c.ccode, c.cdesc, c.term, c.years, c.cred, c.csyllabus, COUNT(r.classid) AS most_prerequisite_class FROM requisite AS r INNER JOIN class AS c ON r.reqid = c.cid WHERE r.prereq = TRUE AND cid != 37 GROUP BY c.cid, c.cname, c.ccode, c.cdesc, c.term, c.years, c.cred, c.csyllabus ORDER BY most_prerequisite_class DESC LIMIT 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMostPerRoom(self, id):
        cursor = self.conn.cursor()
        query = "WITH temp AS ( \
                    SELECT cid, COUNT(cid) as class_count \
                    FROM section \
                    WHERE roomid = %s \
                    GROUP BY cid \
                    ORDER BY class_count DESC \
                    LIMIT 3 \
                ) \
                SELECT class.* \
                FROM class \
                inner JOIN temp ON class.cid = temp.cid \
                ORDER BY temp.class_count DESC;"
        cursor.execute(query, [id])
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getLeastClass(self):
        cursor = self.conn.cursor()
        query = "select class.* from class natural join \
                (select cid, count(*) as cnt from section inner join class using (cid) \
                group by cid) as tp \
                order by tp.cnt \
                limit 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMostPerSemester(self, year, semester):
        cursor = self.conn.cursor()
        query = "WITH temp AS ( \
                        SELECT cid, COUNT(cid) AS count \
                        FROM section AS s \
                        INNER JOIN class USING (cid) \
                        WHERE s.years = %s AND s.semester = %s \
                        GROUP BY cid \
                        ORDER BY count DESC \
                        LIMIT 3 \
                    ) \
                    SELECT class.*, temp.count \
                    FROM class \
                    INNER JOIN temp USING (cid) \
                    ORDER BY temp.count DESC;"
        cursor.execute(query, [year, semester.capitalize()])
        result = []
        for row in cursor:
            result.append(row)
        return result
