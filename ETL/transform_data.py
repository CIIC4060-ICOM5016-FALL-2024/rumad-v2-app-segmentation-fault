import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from numpy import insert
from extract_data import run_etl
from ETL.DAO.insert_DAO import insert_to_db
# from handlers.meeting_handler import insert_meeting
# from handlers.requisites_handler import insert_requisites
# from handlers.room_handler import insert_room
# from handlers.sections_handler import insert_sections


def main():
    # Call the run_etl function
    dataframes = run_etl()

    # Print each dataframe with its table name
    for i, (df, table_name) in enumerate(dataframes):
        insert_to_db(df, table_name)
        
        
        

if __name__ == "__main__":
    main()
