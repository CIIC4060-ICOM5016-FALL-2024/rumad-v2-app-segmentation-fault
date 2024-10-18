from DAO.db_config import pg_config
import psycopg2 as pg
import pandas as pd

def insert_to_db(dataframe, table_name):
    url = "dbname=%s password=%s user=%s host=%s port=%s" % \
          (pg_config['dbname'], pg_config['password'], pg_config['user'], pg_config['host'], pg_config['port'])
    
    try:
        conn = pg.connect(url)
        cursor = conn.cursor()
        
        if table_name == "df_class":
            query = """
            INSERT INTO class (cid, cname, ccode, cdesc, term, years, cred, csyllabus) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        elif table_name == "df_meeting":
            dataframe['starttime'] = pd.to_datetime('1970-01-01 ' + dataframe['starttime'])
            dataframe['endtime'] = pd.to_datetime('1970-01-01 ' + dataframe['endtime'])
            query = """
            INSERT INTO meeting (mid, ccode, starttime, endtime, cdays)
            VALUES (%s, %s, %s, %s, %s)
            """
        elif table_name == "df_requisite":
            dataframe['prereq'] = dataframe['prereq'].map({0: False, 1: True})
            query = """
            INSERT INTO requisite (classid, reqid, prereq)
            VALUES (%s, %s, %s)
            """
        elif table_name == "df_room":
            query = """
            INSERT INTO room (rid, building, room_number, capacity)
            VALUES (%s, %s, %s, %s)
            """
        elif table_name == "df_section":
            query = """
            INSERT INTO section (sid, roomid, cid, mid, semester, years, capacity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        
        # Ejecutar la inserción de los datos
        cursor.executemany(query, dataframe.values) # type: ignore
        
        # Confirmar la transacción
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully into {table_name} table")

    except Exception as e:
        # Si ocurre un error, imprimir el mensaje y hacer rollback
        print(f"Error inserting data into {table_name} table: {e}")
        conn.rollback() # type: ignore
    
    finally:
        # Asegurarse de cerrar el cursor y la conexión
        if cursor: # type: ignore
            cursor.close()
        if conn: # type: ignore
            conn.close()
