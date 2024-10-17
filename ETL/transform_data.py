import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from numpy import insert
from extract_data import run_etl
from handlers.classes_handler import insert_classes
# from handlers.meeting_handler import insert_meeting
# from handlers.requisites_handler import insert_requisites
# from handlers.room_handler import insert_room
# from handlers.sections_handler import insert_sections


def main():
    # Call the run_etl function
    dataframes = run_etl()

    # Print each dataframe with its table name
    for i, (df, table_name) in enumerate(dataframes):
        # print(df)
        
        if table_name == "class":
            # insert_classes(df)
            print(df)
        # elif table_name == "meeting":
        #     insert_meeting(df)
        # elif table_name == "requisite":
        #     insert_requisites(df)
        # elif table_name == "room":
        #     insert_room(df)
        # elif table_name == "section":
        #     insert_sections(df)
        else:
            print(f"Table {table_name} not found")
        

if __name__ == "__main__":
    main()
