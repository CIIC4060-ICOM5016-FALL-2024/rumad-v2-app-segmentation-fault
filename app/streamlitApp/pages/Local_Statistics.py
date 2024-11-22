import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from matplotlib import colors as mcolors
import io
import json

# inyect CSS to style the page
st.markdown(
    """
    <style>
    /* Style for buttons */
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        border-radius: 10px;
    }

    /* Style for tables */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
    }
    .custom-table td, .custom-table th {
        border: 1px solid #ddd;
        padding: 8px;
    }
    .custom-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .custom-table tr:hover {
        background-color: #f1f1f1;
    }
    .custom-table th {
        background-color: #4CAF50;
        color: white;
        text-align: left;
        padding: 8px;
    }

    /* Style for headings */
    h3 {
        color: #333;
        margin-top: 20px;
        font-size: 22px;
    }

    /* General container styling */
    .stMarkdown {
        font-family: Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def generate_green_shades(base_color, values):
    base_rgb = mcolors.hex2color(base_color)
    lighter_rgb = [(c + 1) / 2 for c in base_rgb]  # A lighter version of the base green
    colors = [
        mcolors.to_hex([(1 - value) * light + value * dark for light, dark in zip(lighter_rgb, base_rgb)])
        for value in values
    ]
    return colors

st.title("Local Stats")

top_three_rooms_per_capacity_container = st.container()
top_three_rooms_per_ration_container = st.container()
top_three_classes_taught_per_semester_container = st.container()
top_three_classes_taught_per_room_container = st.container()
key = 0 # key for download syllabus button to avoid caching issues


with top_three_rooms_per_capacity_container:
    st.subheader("Top 3 rooms with the most capacity")
    st.divider()
    building = "Stefani"
    buildings = ["Stefani", "Software", "Monzon"]
    for i, col in enumerate(st.columns(3)):
        with col:
            if st.button(buildings[i], key=f"capacity_button_{buildings[i]}"):
                building = buildings[i]
    try:
        response = requests.post(f"https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/room/{building}/capacity")
        if response.status_code == 200:
            data = response.json()
            df = pd.json_normalize(data)

            df["normalized_capacity"] = (df["capacity"] - df["capacity"].min()) / (df["capacity"].max() - df["capacity"].min())
            df["colors"] = generate_green_shades("#327136", df["normalized_capacity"])


            fig_stacked = px.bar(
                df,
                x="capacity",
                color="room_number",
                color_discrete_sequence=df["colors"],  
                labels={"Capacity": "Room Capacity", "Building": "Building Name"},
                orientation="h",
            )
            fig_stacked.update_layout(
                xaxis=dict(
                    showline=True,  # Show boundary line for x-axis
                    linewidth=2,  # Line width
                    linecolor="black",  # Line color
                    showgrid=True,  # Enable gridlines
                    gridcolor="lightgray",  # Gridline color
                    gridwidth=0.5,  # Gridline width
                ),
                yaxis=dict(
                    categoryorder="total ascending",
                    showline=True,  # Show boundary line for y-axis
                    linewidth=2,  # Line width
                    linecolor="black",  # Line color
                ),
                plot_bgcolor="white",  # Set background color to white
            )
            st.plotly_chart(fig_stacked)
        else:
            st.write("Error: " + response.status_code)
    except:
        st.write("Error: Could not connect to the API.")

with top_three_rooms_per_ration_container:
    st.subheader("Top 3 sections with the most student-to-capacity ratio.")
    st.divider()
    building = "Stefani"
    buildings = ["Stefani", "Software", "Monzon"]
    for i, col in enumerate(st.columns(3)):
        with col:
            if st.button(buildings[i], key=f"ratio_button_{buildings[i]}"):
                building = buildings[i]

    try:
        response = requests.post(f"https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/room/{building}/ratio")
        if response.status_code == 200:
            data = response.json()
            df = pd.json_normalize(data)

            df["colors"] = generate_green_shades("#327136", df["ratio"])


            fig_stacked = px.bar(
                df,
                x="ratio",
                color="room_number",
                color_discrete_sequence=df["colors"],  
                labels={"Capacity": "Room Capacity", "Building": "Building Name"},
                orientation="h",
            )
            fig_stacked.update_layout(
                xaxis=dict(
                    showline=True,  # Show boundary line for x-axis
                    linewidth=2,  # Line width
                    linecolor="black",  # Line color
                    showgrid=True,  # Enable gridlines
                    gridcolor="lightgray",  # Gridline color
                    gridwidth=0.5,  # Gridline width
                ),
                yaxis=dict(
                    categoryorder="total ascending",
                    showline=True,  # Show boundary line for y-axis
                    linewidth=2,  # Line width
                    linecolor="black",  # Line color
                ),
                plot_bgcolor="white",  # Set background color to white
            )
            st.plotly_chart(fig_stacked)
        else:
            st.write("Error: " + response.status_code)
    except:
        st.write("Error: Could not connect to the API.")

with top_three_classes_taught_per_semester_container:
    st.subheader("Top 3 most taught classes per semester.")
    st.divider()
    semester = "Fall"
    year = "2018"
    years = [str(i) for i in range(2017, 2026)]
    semesters = ["Fall", "Spring"]

    col_year, col_sem = st.columns(2)

    with col_year:
        year = st.selectbox("Select a year", years, key="year")
    with col_sem:
        semester = st.selectbox("Select a semester", semesters, key="semester")

    try:
        response = requests.post(f"https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/classes/{year}/{semester}")
        if response.status_code == 200:
            data = response.json()
            for i, class_info in enumerate(data):
                st.markdown(f"""
                    <h3>Class {i + 1}</h3>
                    <table class="custom-table">
                        <tr>
                            <th>Field</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Code</td>
                            <td>{class_info["cname"]} ({class_info["ccode"]})</td>
                        </tr>
                        <tr>
                            <td>Description</td>
                            <td>{class_info["cdesc"]}</td>
                        </tr>
                        <tr>
                            <td>Class ID</td>
                            <td>{class_info["cid"]}</td>
                        </tr>
                        <tr>
                            <td>Credits</td>
                            <td>{class_info["cred"]}</td>
                        </tr>
                        <tr>
                            <td>Term</td>
                            <td>{class_info["term"]}</td>
                        </tr>
                        <tr>
                            <td>Years</td>
                            <td>{class_info["years"]}</td>
                        </tr>
                    </table>
                    <hr>
                """, unsafe_allow_html=True)
                try:
                    syllabus_url = class_info["csyllabus"]
                    if syllabus_url == 'None':
                        st.write("No syllabus available for this class.")
                    else:
                        file_response = requests.get(syllabus_url)
                        if file_response.status_code == 200:
                            # Prepare file content for download
                            file_bytes = io.BytesIO(file_response.content)
                            st.download_button(
                                label="Download Syllabus",
                                data=file_bytes,
                                file_name=f"{class_info['ccode']}_syllabus.pdf",
                                mime="application/pdf",
                                key=f"download_syllabus_{class_info['cid'], key}"
                            )
                            key += 1
                        else:
                            st.write("Error: Could not fetch the syllabus file.")
                except Exception as e:
                    st.write("Error downloading syllabus:", e)
        else:
            st.write("Error: " + str(response.status_code))
    except Exception as e:
        st.write("Error: Could not connect to the API.")
        st.write(e)

with top_three_classes_taught_per_room_container:
    st.subheader("Top 3 classes that were taught the most per building per room.")
    st.divider()
    rids = []
    try:
        # Fetch room IDs
        response = requests.get("https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/room")
        df = pd.json_normalize(response.json())
        rids = df["rid"].tolist()
    except Exception as e:
        st.write("Error: Could not connect to the API.")
        st.write(e)

    # Display room selection
    selected_rid = st.selectbox("Select a room", rids)
    
    if selected_rid:  # Ensure a room is selected
        try:
            # Fetch classes for the selected room
            response = requests.post(f"https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/room/{selected_rid}/classes")
            if response.status_code == 200:
                data = response.json()
                for i, class_info in enumerate(data):
                    st.markdown(f"""
                        <h3>Class {i + 1}</h3>
                        <table class="custom-table">
                            <tr>
                                <th>Field</th>
                                <th>Value</th>
                            </tr>
                            <tr>
                                <td>Code</td>
                                <td>{class_info["cname"]} ({class_info["ccode"]})</td>
                            </tr>
                            <tr>
                                <td>Description</td>
                                <td>{class_info["cdesc"]}</td>
                            </tr>
                            <tr>
                                <td>Class ID</td>
                                <td>{class_info["cid"]}</td>
                            </tr>
                            <tr>
                                <td>Count</td>
                                <td>{class_info["class_count"]}</td>
                            </tr>
                            <tr>
                                <td>Credits</td>
                                <td>{class_info["cred"]}</td>
                            </tr>
                            <tr>
                                <td>Term</td>
                                <td>{class_info["term"]}</td>
                            </tr>
                            <tr>
                                <td>Years</td>
                                <td>{class_info["years"]}</td>
                            </tr>
                        </table>
                        <hr>
                    """, unsafe_allow_html=True)
                    
                    try:
                        syllabus_url = class_info["csyllabus"]
                        if syllabus_url == 'None':
                            st.write("No syllabus available for this class.")
                        else:
                            file_response = requests.get(syllabus_url)
                            if file_response.status_code == 200:
                                # Prepare file content for download
                                file_bytes = io.BytesIO(file_response.content)
                                st.download_button(
                                    label="Download Syllabus",
                                    data=file_bytes,
                                    file_name=f"{class_info['ccode']}_syllabus.pdf",
                                    mime="application/pdf",
                                    key=f"download_syllabus_{class_info['cid'], key}"
                                )
                                key += 1
                            else:
                                st.write("Error: Could not fetch the syllabus file.")
                    except Exception as e:
                        st.write("Error downloading syllabus:", e)
            else:
                st.write("Error: " + str(response.status_code))
        except Exception as e:
            st.write("Error: Could not connect to the API.")
            st.write(e)



        
#327136

