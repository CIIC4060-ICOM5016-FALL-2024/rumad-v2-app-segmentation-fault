from DAO.db_config import pg_config
import psycopg2 as pg

def insert_classes(dataframe):
    url = "dbname=%s password=%s user=%s host=%s port=%s" % \
          (pg_config['dbname'], pg_config['password'], pg_config['user'], pg_config['host'], pg_config['port'])
    
    try:
        conn = pg.connect(url)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO class (cid, cname, ccode, cdesc, term, years, cred, csyllabus) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Ejecutar la inserción de los datos
        cursor.executemany(query, dataframe.values)
        
        # Confirmar la transacción
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully into 'classes' table")

    except Exception as e:
        # Si ocurre un error, imprimir el mensaje y hacer rollback
        print(f"Error inserting data into 'class' table: {e}")
        conn.rollback() # type: ignore
    
    finally:
        # Asegurarse de cerrar el cursor y la conexión
        if cursor: # type: ignore
            cursor.close()
        if conn: # type: ignore
            conn.close()
