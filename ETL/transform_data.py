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

    # 1. Ensure that classes have ID starting from 2
    df_class["cid"] = pd.to_numeric(df_class["cid"], errors="coerce")
    df_class.dropna(subset=["cid"], inplace=True)
    df_class = df_class[df_class["cid"] >= 2]

    # 2. Ensure no overlapping sections && 3. Ensure sections of a class are taught at different hours
    df_section_meeting = df_section.merge(df_meeting, on="mid")
    df_section_meeting = df_section_meeting.sort_values(
        ["roomid", "starttime", "endtime"]
    )

    # Detect overlapping sections
    overlaps = []
    for roomid, group in df_section_meeting.groupby("roomid"):
        for i in range(1, len(group)):
            previous = group.iloc[i - 1]
            current = group.iloc[i]

            # Check if current start time overlaps with the previous end time
            if current["starttime"] < previous["endtime"]:
                # If overlapping, add the one with the higher sid to the list of sections to remove
                if current["sid"] > previous["sid"]:
                    overlaps.append(current["sid"])
                else:
                    overlaps.append(previous["sid"])

    # Remove overlapping sections with the higher sid
    df_section = df_section[~df_section["sid"].isin(overlaps)]

    # 4. Adjust 'MJ' meetings and remove overlaps
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

    # 5. Ensure correct durations for 'LMV' and 'MJ' meetings
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

    # 7. Ensure sections do not exceed room capacity

    # 8. Ensure sections are taught in the correct semester and year

    # 9. Ensure sections reference valid classrooms, meetings, and classes

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


if __name__ == "__main__":
    clean_data()

    # dataframes[0][0] = courses/class
    # cid	cname	ccode	cdesc	term	years	cred	csyllabus

    # dataframes[1][0] = room
    # rid	building	room_number	capacity

    # dataframes[2][0] = section
    # sid	roomid	cid	mid	semester	years	capacity

    # dataframes[3][0] = meeting
    # mid	ccode	starttime	endtime	cdays

    # dataframes[4][0] = requisite
    # classid	reqid	prereq
