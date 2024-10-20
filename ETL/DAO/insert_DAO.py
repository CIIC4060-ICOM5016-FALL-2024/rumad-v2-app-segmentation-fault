from DAO.db_config import pg_config
import psycopg2 as pg
import pandas as pd

def insert_to_db(dataframe, table_name):
    # Create the connection string
    url = "dbname=%s password=%s user=%s host=%s port=%s" % \
          (pg_config['dbname'], pg_config['password'], pg_config['user'], pg_config['host'], pg_config['port'])
    
    # Connect to the database and insert the data
    try:
        conn = pg.connect(url)
        cursor = conn.cursor()
        
        # Create the query based on the table name
        if table_name == "class":
            query = """
            INSERT INTO class (cid, cname, ccode, cdesc, term, years, cred, csyllabus) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        elif table_name == "meeting":
            dataframe['starttime'] = dataframe['starttime'].astype(str)
            dataframe['endtime'] = dataframe['endtime'].astype(str)
            dataframe['starttime'] = pd.to_datetime('1970-01-01 ' + dataframe['starttime'])
            dataframe['endtime'] = pd.to_datetime('1970-01-01 ' + dataframe['endtime'])
            query = """
            INSERT INTO meeting (mid, ccode, starttime, endtime, cdays)
            VALUES (%s, %s, %s, %s, %s)
            """
        elif table_name == "requisite":
            dataframe['prereq'] = dataframe['prereq'].map({0: False, 1: True})
            query = """
            INSERT INTO requisite (classid, reqid, prereq)
            VALUES (%s, %s, %s)
            """
        elif table_name == "room":
            query = """
            INSERT INTO room (rid, building, room_number, capacity)
            VALUES (%s, %s, %s, %s)
            """
        elif table_name == "section":
            query = """
            INSERT INTO section (sid, roomid, cid, mid, semester, years, capacity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        elif table_name == "syllabus":
            query = """
            INSERT INTO syllabus (chunkid, courseid, embedding_text, chunk)
            VALUES (%s, %s, %s, %s)
            """
        else:
            print("Table name not recognized")
            return
        
        # Execute the query
        cursor.executemany(query, dataframe.values) # type: ignore
        
        # Commit the transaction
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully into {table_name} table")

    except Exception as e:
        # Rollback the transaction in case of an error
        print(f"Error inserting data into {table_name} table: {e}")
        conn.rollback() # type: ignore
    
    finally:
        # Close the cursor and connection
        if cursor: # type: ignore
            cursor.close()
        if conn: # type: ignore
            conn.close()
