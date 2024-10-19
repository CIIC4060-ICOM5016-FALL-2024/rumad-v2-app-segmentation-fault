from extract_data import run_etl
import pandas as pd
import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
    # Function to convert 'HH:MM:SS' format to minutes
    def convert_to_minutes(time_str):
        hours, minutes, _ = map(int, time_str.split(":"))
        return hours * 60 + minutes

    # Function to convert minutes back to 'HH:MM' format
    def convert_to_hhmm(total_minutes):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours}:{minutes:02d}"

    # Convert 'starttime' and 'endtime' columns to minutes for easier manipulation
    df_meeting[["starttime", "endtime"]] = df_meeting[
        ["starttime", "endtime"]
    ].applymap(convert_to_minutes)

    # Filter out meetings on 'MJ' days between 10:15 and 12:30
    df_meeting = df_meeting[
        ~(
            (df_meeting["cdays"] == "MJ")
            & (df_meeting["starttime"] > convert_to_minutes("10:15:00"))
            & (df_meeting["endtime"] < convert_to_minutes("12:30:00"))
        )
    ]

    # Function to find the index of the earliest and latest class based on condition
    def find_class_index(condition):
        try:
            return df_meeting[condition].index[0]
        except IndexError:
            return -1

    # Find earliest and latest class times between 10:15 and 12:30 on 'MJ' days
    index_earliest_class_after_1030 = find_class_index(
        (df_meeting["cdays"] == "MJ")
        & (df_meeting["starttime"] > convert_to_minutes("10:15:00"))
        & (df_meeting["starttime"] < convert_to_minutes("12:30:00"))
    )

    index_latest_class_before_1230 = find_class_index(
        (df_meeting["cdays"] == "MJ")
        & (df_meeting["endtime"] < convert_to_minutes("12:30:00"))
        & (df_meeting["endtime"] > convert_to_minutes("10:15:00"))
    )

    # Adjust class timings if valid indices are found
    if index_earliest_class_after_1030 != -1:
        delta_time = (
            convert_to_minutes("12:30:00")
            - df_meeting.loc[index_earliest_class_after_1030, "starttime"]
        )
        df_meeting.loc[
            (df_meeting["cdays"] == "MJ")
            & (df_meeting.index >= index_earliest_class_after_1030),
            ["starttime", "endtime"],
        ] += delta_time

    if index_latest_class_before_1230 != -1:
        delta_time = df_meeting.loc[
            index_earliest_class_after_1030, "endtime"
        ] - convert_to_minutes("10:15:00")
        df_meeting.loc[
            (df_meeting["cdays"] == "MJ")
            & (df_meeting.index <= index_latest_class_before_1230),
            ["starttime", "endtime"],
        ] -= delta_time

    # Remove all meetings that start after 19:45
    df_meeting = df_meeting[df_meeting["starttime"] <= convert_to_minutes("19:45:00")]

    # Convert 'starttime' and 'endtime' columns back to 'HH:MM' format
    df_meeting[["starttime", "endtime"]] = df_meeting[
        ["starttime", "endtime"]
    ].applymap(convert_to_hhmm)

    # Convert 'starttime' and 'endtime' back to datetime.time format for display purposes
    df_meeting["starttime"] = pd.to_datetime(
        df_meeting["starttime"], format="%H:%M"
    ).dt.time
    df_meeting["endtime"] = pd.to_datetime(
        df_meeting["endtime"], format="%H:%M"
    ).dt.time

    print(f"Length of df_section: {len(df_section)}")

    ################################################################################################
    # 5. All ‘LWV’ sections have the correct hours
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
    df_section_class = df_section.merge(df_class, on="cid")
    years_x = pd.to_numeric(df_section_class["years_x"], errors="coerce")

    # Delete classes sections with Authorization from the Director of the Department needed
    df_section_class = df_section_class[
        df_section_class["cname"] != "Authorization from the Director of the Department"
    ]

    # Boolean Conditions
    First_semester = (
        (df_section_class["term"] == "First Semester")
        | (df_section_class["term"] == "First Semester, Second Semester")
    ) & (df_section_class["semester"] == "Fall")
    Second_semester = (
        (df_section_class["term"] == "Second Semester")
        | (df_section_class["term"] == "First Semester, Second Semester")
    ) & (df_section_class["semester"] == "Spring")
    According_Demand = (df_section_class["term"] == "According to Demand") & (
        (df_section_class["semester"] == "Fall")
        | (df_section_class["semester"] == "Spring")
        | (df_section_class["semester"] == "V1")
        | (df_section_class["semester"] == "V2")
    )
    Even_year = (df_section_class["years_y"] == "Even Years") & ((years_x % 2) == 0)
    Odd_year = (df_section_class["years_y"] == "Odd Years") & ((years_x % 2) != 0)
    Every_Year = df_section_class["years_y"] == "Every Year"
    According_Demand_Year = df_section_class["years_y"] == "According to Demand"

    # Combine the boolean conditions into a single series
    combined_conditions = (First_semester | Second_semester | According_Demand) & (
        Even_year | Odd_year | Every_Year | According_Demand_Year
    )

    # Ensure the combined_conditions series has the same index as df_section_class
    combined_conditions = combined_conditions.reindex(df_section_class.index)

    # Filter the sections based on the combined boolean conditions
    df_section_class = df_section_class[combined_conditions]
    # Update the section dataframe
    df_section = df_section[df_section["sid"].isin(df_section_class["sid"])]

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
    # print(df_class)
    # print(df_section)
    # print(df_meeting)
    # print(df_room)
    # print(df_requisite)

    return [
        (df_room, "room"),
        (df_meeting, "meeting"),
        (df_class, "class"),
        (df_requisite, "requisite"),
        (df_section, "section"),
    ]


if __name__ == "__main__":
    clean_data()
