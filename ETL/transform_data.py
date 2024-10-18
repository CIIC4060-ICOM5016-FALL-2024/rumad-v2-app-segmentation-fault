from extract_data import run_etl
import pandas as pd


def update_names():
    # get all dataframes as a dictionary of (df, table_name)
    dataframes = run_etl()

    # Create a dictionary to hold the dataframes
    df_dict = {}
    for df, table_name in dataframes:
        df_dict[f"df_{table_name}"] = df
    return df_dict


# Transform the data
def clean_data():
    df_dict = update_names()

    # Remove rows with null values across all dataframes
    df_dict["df_class"].dropna(inplace=True)
    df_dict["df_section"].dropna(inplace=True)
    df_dict["df_meeting"].dropna(inplace=True)
    df_dict["df_room"].dropna(inplace=True)
    df_dict["df_requisite"].dropna(inplace=True)

    # Init the dataframes
    df_class = df_dict["df_class"]
    df_section = df_dict["df_section"]
    df_meeting = df_dict["df_meeting"]
    df_room = df_dict["df_room"]
    df_requisite = df_dict["df_requisite"]

    ################################################################################################
    # 1. Ensure that classes have ID starting from 2
    ################################################################################################
    df_class["cid"] = pd.to_numeric(df_class["cid"], errors="coerce")
    df_class.dropna(subset=["cid"], inplace=True)
    df_class = df_class[df_class["cid"] >= 2]
    df_section = df_section[df_section["cid"] >= 2]

    ################################################################################################
    # 2. Two sections cannot be taught at the same hour in the same classroom.
    # 3. A class cannot have the same section, they must be taught at different hours.
    ################################################################################################

    # Delete sections with duplicate 'sid'
    df_section = df_section.drop_duplicates(subset=["sid"], keep=False)

    # Merge 'section' with 'meeting' to check for overlapping sections in the same room, time, and semester
    df_section_meeting = df_section.merge(df_meeting, on="mid")

    # Convert 'starttime' and 'endtime' to time objects
    df_section_meeting["starttime"] = pd.to_datetime(
        df_section_meeting["starttime"], format="%H:%M:%S"
    ).dt.time
    df_section_meeting["endtime"] = pd.to_datetime(
        df_section_meeting["endtime"], format="%H:%M:%S"
    ).dt.time

    # Sort the dataframe by room, semester, starttime, and sid
    df_section_meeting = df_section_meeting.sort_values(
        ["roomid", "semester", "starttime", "sid"]
    )

    # Detect overlapping sections (same room, same semester, same time)
    overlaps = []
    for (roomid, semester, starttime, cdays), group in df_section_meeting.groupby(
        ["roomid", "semester", "starttime", "cdays"]
    ):
        for i in range(1, len(group)):
            previous = group.iloc[i - 1]
            current = group.iloc[i]

            # Check if sections overlap in the same room, same time, and same semester
            if (
                current["starttime"] == previous["starttime"]
                and current["roomid"] == previous["roomid"]
                and current["semester"] == previous["semester"]
                and current["years"] == previous["years"]
                and current["cdays"] == previous["cdays"]
            ):
                # Add the section with the higher sid to the list of overlaps to delete
                if current["sid"] > previous["sid"]:
                    overlaps.append(current["sid"])
                else:
                    overlaps.append(previous["sid"])

    # Remove overlapping sections with the higher sid
    df_section = df_section[~df_section["sid"].isin(overlaps)]

    ################################################################################################
    # 4. Adjust 'MJ' meetings and remove overlaps
    ################################################################################################
    '''
    def timeTransfer(mid, dataFrame, timeChange, direction):
        for index, row in dataFrame.iterrows():
            if row['mid'] == mid:
                meeting_index = index
                dataFrame.at[meeting_index, 'starttime'] = row['starttime'] + timeChange
                dataFrame.at[meeting_index, 'endtime'] = row['endtime'] + timeChange
                break

        if direction == 'backwards':
            sliding_meetings_index = range(meeting_index)

        else:
            sliding_meetings_index = range(meeting_index + 1, len(dataFrame))
        
        for index in sliding_meetings_index:
            dataFrame.at[index, 'starttime'] = dataFrame.at[index, 'starttime'] + timeChange
            dataFrame.at[index, 'endtime'] = dataFrame.at[index, 'endtime'] + timeChange
        

    
    df_meeting["starttime"] = pd.to_datetime(
        df_meeting["starttime"], format="%H:%M:%S"
    ).dt.time
    df_meeting["endtime"] = pd.to_datetime(
        df_meeting["endtime"], format="%H:%M:%S"
    ).dt.time

    # Remove all 'MJ' meetings with start time after 10:15 AM and end time before 12:30 PM
    df_meeting = df_meeting[
        ~(
            (df_meeting["cdays"] == "MJ")
            & (df_meeting["starttime"] > pd.to_datetime("10:15", format="%H:%M").time())
            & (df_meeting["endtime"] < pd.to_datetime("12:30", format="%H:%M").time())
        )
    ]

    # Remove all meetings that start after 19:45
    df_meeting = df_meeting[
        df_meeting["starttime"] <= pd.to_datetime("19:45", format="%H:%M").time()
    ]
    
        
    # TODO TIME TRANSFER datetime.time - datetime.time error

    # Manage overlaps
    for index, row in df_meeting.iterrows():
        if (row['cdays'] == 'MJ') \
            & (((row['starttime'] >= pd.to_datetime("7:30", format="%H:%M").time()) & (row['starttime'] <= (pd.to_datetime("10:15", format="%H:%M").time()))) \
            & ~((row['endtime'] >= pd.to_datetime("7:30", format="%H:%M").time()) & (row['endtime'] <= pd.to_datetime("10:15", format="%H:%M").time()))):
            
            timeTransfer(row['mid'], df_meeting,pd.to_datetime("10:15", format="%H:%M") - pd.to_datetime(row['endtime'].strftime('%H:%M'), format="%H:%M"), 'backwards')

        elif (row['cdays'] == 'MJ') \
            & (~((row['starttime'] >= pd.to_datetime("12:30", format="%H:%M").time()) & (row['starttime'] <= (pd.to_datetime("19:45", format="%H:%M").time()))) \
            & ((row['endtime'] >= pd.to_datetime("12:30", format="%H:%M").time()) & (row['endtime'] <= pd.to_datetime("19:45", format="%H:%M").time()))):

            timeTransfer(row['mid'], df_meeting, pd.to_datetime("12:30", format="%H:%M") - pd.to_datetime(row['starttime'].strftime('%H:%M'), format="%H:%M"), 'forwards')
            '''


    ################################################################################################
    # 5. All ‘LWV’ sections have the correct hours
    ################################################################################################

    ################################################################################################
    # 6. ‘LWV’ meetings have a duration of 50 minutes; ‘MJ’ meetings have a duration of 75 minutes.
    ################################################################################################
    df_meeting.loc[df_meeting["cdays"] == "LWV", "duration"] = 50
    df_meeting.loc[df_meeting["cdays"] == "MJ", "duration"] = 75

    df_meeting = df_meeting[
        (
            (df_meeting["cdays"] == "LWV")
            & (
                pd.to_datetime(df_meeting["endtime"], format="%H:%M:%S")
                - pd.to_datetime(df_meeting["starttime"], format="%H:%M:%S")
                == pd.Timedelta(minutes=50)
            )
        )
        | (
            (df_meeting["cdays"] == "MJ")
            & (
                pd.to_datetime(df_meeting["endtime"], format="%H:%M:%S")
                - pd.to_datetime(df_meeting["starttime"], format="%H:%M:%S")
                == pd.Timedelta(minutes=75)
            )
        )
    ]

    df_meeting.drop(columns=["duration"], inplace=True)

    ################################################################################################
    # 7. Sections cannot be in overcapacity, classrooms have limits.
    ################################################################################################
    df_section_room = df_section.merge(df_room, left_on="roomid", right_on="rid")
    df_section_room = df_section_room[
        df_section_room["capacity_x"] <= df_section_room["capacity_y"]
    ]
    df_section = df_section[df_section["sid"].isin(df_section_room["sid"])]

    ################################################################################################
    # 8. Courses must be taught in the correct year and correct semester.
    ################################################################################################
    
    df_section_class = df_section.merge(df_class, on='cid')
    df_section_class = df_section_class[df_section_class['cid'] != 37]
    years_x =  pd.to_numeric(df_section_class["years_x"], errors="coerce")
    # Boolean Conditions
    First_semester = ((df_section_class["term"] == "First Semester" ) | (df_section_class["term"] == "First Semester, Second Semester")) & (df_section_class["semester"] == "Fall")
    Second_semester = ((df_section_class["term"] == "Second Semester") | (df_section_class["term"] == "First Semester, Second Semester")) & (df_section_class["semester"] == "Spring")
    According_Demand = (df_section_class["term"] == "According to Demand") & (
        (df_section_class["semester"] == "Fall")
        | (df_section_class["semester"] == "Spring")
        | (df_section_class["semester"] == "V1")
        | (df_section_class["semester"] == "V2")
    )  
    Even_year = (
        (df_section_class["years_y"] == "Even Years")
        & ((years_x % 2) == 0)
    )
    Odd_year = (
        (df_section_class["years_y"] == "Odd Years")
        & ((years_x % 2) != 0)
    )
    Every_Year = (
        (df_section_class["years_y"] == "Every Year")
    )
    According_Demand_Year = (df_section_class["years_y"] == "According to Demand")

    # Filter the sections based on the boolean conditions
    df_section_class = df_section_class[
        ~((First_semester | Second_semester | According_Demand)
        &
        (Even_year | Odd_year | Every_Year | According_Demand_Year))
    ]
    #Update the section dataframe 
    df_section = df_section[~df_section["sid"].isin(df_section_class["sid"])]
    
    ################################################################################################
    # 9. Sections must be taught in a valid classroom and meeting, and the class must exist.
    ################################################################################################
    df_section = df_section[df_section["roomid"].isin(df_room["rid"])]
    df_section = df_section[df_section["mid"].isin(df_meeting["mid"])]
    df_section = df_section[df_section["cid"].isin(df_class["cid"])]
    

    ################################################################################################
    # 10. Delete all section with Dummy class as Foreign Key
    ################################################################################################
    dummy_class_ids = df_class[
        df_class["cname"] == "Authorization from the Director of the Department"
    ]["cid"].tolist()

    df_section = df_section[~df_section["cid"].isin(dummy_class_ids)]

    # Print dataframes after cleaning (for verification)
    # print("Cleaned Class DataFrame:")
    # print(df_class)

    # print("Cleaned Section DataFrame:")
    # print(df_section)

    # print("Cleaned Meeting DataFrame:")
    print(df_meeting)

    # print("Cleaned Room DataFrame:")
    # print(df_room)

    # print("Cleaned Requisite DataFrame:")
    # print(df_requisite)

    # Total Tuples
    
    ultra_merge = df_section.merge(df_class, on='cid') \
                        .merge(df_meeting, on='mid') \
                        .merge(df_requisite, left_on = 'cid', right_on = 'classid') \
                        .merge(df_room, left_on='roomid', right_on='rid')
    
    
    df_class = ultra_merge[ultra_merge['cid'].isin(df_class['cid'])].drop_duplicates(subset=['cid'])
    df_meeting = ultra_merge[ultra_merge['mid'].isin(df_class['mid'])].drop_duplicates(subset=['mid'])
    df_requisite = ultra_merge[ultra_merge['classid'].isin(df_class['classid'])].drop_duplicates(subset=['reqid', 'cid'])
    df_room = ultra_merge[ultra_merge['rid'].isin(df_class['rid'])].drop_duplicates(subset=['rid'])
    df_section = df_section.drop_duplicates(subset=['sid'])

    # Print cuantity the count of tuples in all dataframes
    print(f"Dataframes Total Tuples: {len(df_class) + len(df_section) + len(df_meeting) + len(df_requisite) + len(df_room) + len(df_section)}")
  
    print(df_requisite)


if __name__ == "__main__":
    clean_data()
