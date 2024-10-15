import os
import pandas as pd
import sqlite3
import json
import xml.etree.ElementTree as ET
import urllib.request


# Paths for raw data (input) and processed data (output)
RAW_DATA_FOLDER = "./data"


# Function to extract data from SQLite database
def extract_db(file_path):
    conn = sqlite3.connect(file_path)
    table_name = "requisites"
    df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df


# Function to extract data from XML File
def extract_xml(file_path):
    try:
        xmlFile = ET.parse(file_path)
        rows = []
        col = []
        fullcycle = False
        for courses in xmlFile.getroot():
            temp = []

            for l in courses:
                if l.tag == "classes":
                    for m in l:
                        temp.append(m.text)
                        if fullcycle == False:
                            col.append(m.tag)

                else:
                    temp.append(l.text)
                    if fullcycle == False:
                        col.append(l.tag)

            fullcycle = True
            rows.append(temp)

        data_frame = pd.DataFrame(rows, columns=col)
        syllabus_downloader("syllabuses", data_frame)
        return data_frame

    except Exception as Exc:
        print("Exception opening the file, ", Exc)


# Function to Dowlnoad Syllabuses
def syllabus_downloader(folder_name, data_frame):

    SYLLABUS_FOLDER = folder_name

    os.makedirs(SYLLABUS_FOLDER, exist_ok=True)

    try:
        urllist = data_frame["syllabus"].to_list()
        deplist = data_frame["name"].to_list()
        codelist = data_frame["code"].to_list()
        desclist = data_frame["description"].tolist()
        for i in range(len(urllist)):
            if urllist[i] == "None":
                continue
            url = urllist[i]
            desclist[i] = desclist[i].replace(" ", "-")
            file_name = deplist[i] + "-" + codelist[i] + "-" + desclist[i] + ".pdf"
            urllib.request.urlretrieve(url, os.path.join(SYLLABUS_FOLDER, file_name))

    except Exception as Excd:
        print("Exception, cant dowload this file", Excd)


def run_etl():
    dataframes = []  # List to store all dataframes

    # Iterate over all files in the raw_data folder
    for file_name in os.listdir(RAW_DATA_FOLDER):
        file_path = os.path.join(RAW_DATA_FOLDER, file_name)

        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
            if df is not None:
                processed_data = df.dropna()
                dataframes.append(processed_data)

        elif file_name.endswith(".db"):
            df = extract_db(file_path)
            if df is not None:
                processed_data = df.dropna()
                dataframes.append(processed_data)

        elif file_name.endswith(".json"):
            with open(file_path, "r") as f:
                df = json.load(f)
                if df is not None:
                    processed_data = pd.DataFrame(
                        [
                            (item["id"], key, item["number"], item["capacity"])
                            for key, values in df.items()
                            for item in values
                        ],
                        columns=["rid", "Building", "Number", "Capacity"],
                    )

                dataframes.append(processed_data)

        elif file_name.endswith(".xml"):
            df = extract_xml(file_path)
            dataframes.append(df)

    return dataframes


if __name__ == "__main__":
    run_etl()
