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
        df_section_meeting["starttime"]
    ).dt.time
    df_section_meeting["endtime"] = pd.to_datetime(
        df_section_meeting["endtime"]
    ).dt.time

    # Sort the dataframe by room, semester, starttime, and sid
    df_section_meeting = df_section_meeting.sort_values(
        ["roomid", "semester", "starttime", "sid"]
    )

    # Detect overlapping sections (same room, same semester, same time)
    overlaps = []
    for (roomid, semester, starttime), group in df_section_meeting.groupby(
        ["roomid", "semester", "starttime"]
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
    df_meeting["starttime"] = pd.to_datetime(df_meeting["starttime"]).dt.time
    df_meeting["endtime"] = pd.to_datetime(df_meeting["endtime"]).dt.time

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
    print(df_section)

    # print("Cleaned Meeting DataFrame:")
    # print(df_meeting)

    # print("Cleaned Room DataFrame:")
    # print(df_room)

    # print("Cleaned Requisite DataFrame:")
    # print(df_requisite)


if __name__ == "__main__":
    clean_data()
