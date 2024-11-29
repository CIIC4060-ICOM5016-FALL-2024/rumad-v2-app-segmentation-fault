from numpy import NaN
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from matplotlib import colors as mcolors
import io

st.set_page_config(
    page_title="Global Stats",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="./logos/seal-rum-uprm-1280x1280px.png"
) 

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

st.title("Global Stats")

top_five_meetings_with_most_sections_container = st.container()
top_three_classes_as_prerequisite_container = st.container()
top_three_classes_offered_least_container = st.container()
total_sections_per_year_container = st.container()
key = 0 # key for download syllabus button to avoid caching issues

if st.session_state.get("login"):

    with top_five_meetings_with_most_sections_container:
        st.subheader("Top 5 meetings with the most sections.")
        st.divider()
        # try:
        response = requests.post("https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/most/meeting")
        # if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data)
        df["normalized_section_count"] = (df["section_count"] - df["section_count"].min()) / (df["section_count"].max() - df["section_count"].min())
        df["colors"] = generate_green_shades("#327136", df["normalized_section_count"])

        fig = px.bar(
            df, 
            x="mid", 
            y="section_count", 
            labels={"section_count": "Number of sections", "mid": "Meeting ID"},
            )
        fig.update_traces(marker_color="#327136")
        
        fig.update_layout(
            xaxis=dict(
                type="category",
                # categoryorder="total ascending",
                showline=True,  # Show boundary line for x-axis
                linewidth=2,  # Line width
                linecolor="black",  # Line color
                showgrid=True,  # Enable gridlines
                gridcolor="lightgray",  # Gridline color
                gridwidth=0.5,  # Gridline width
            ),
            yaxis=dict(
                showline=True,  # Show boundary line for y-axis
                linewidth=2,  # Line width
                linecolor="black",  # Line color
            ),
            plot_bgcolor="white",  # Set background color to white
        )
        st.plotly_chart(fig)
        #     else:
        #         st.error("Failed to fetch data from the API.")
        # except:
        #     st.error("Failed to fetch data from the API.")


        

    with top_three_classes_as_prerequisite_container:
        st.subheader("Top 3 classes with the most prerequisites")
        st.divider()

        response = requests.post("https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/most/prerequisite")
        if response.status_code == 200:
                data = response.json()
                df = pd.json_normalize(data)
                df["normalized_prerequisite_count"] = (df["prerequisite_classes"] - df["prerequisite_classes"].min()) / (df["prerequisite_classes"].max() - df["prerequisite_classes"].min())
                df["colors"] = generate_green_shades("#327136", df["normalized_prerequisite_count"])

                fig = px.bar(
                    df, 
                    x="cid", 
                    y="prerequisite_classes", 
                    labels={"prerequisite_classes": "Number of prerequisite", "cid": "Class ID"},
                    )
                fig.update_traces(marker_color="#327136")
                
                fig.update_layout(
                    xaxis=dict(
                        type="category",
                        # categoryorder="total ascending",
                        showline=True,  # Show boundary line for x-axis
                        linewidth=2,  # Line width
                        linecolor="black",  # Line color
                        showgrid=True,  # Enable gridlines
                        gridcolor="lightgray",  # Gridline color
                        gridwidth=0.5,  # Gridline width
                    ),
                    yaxis=dict(
                        showline=True,  # Show boundary line for y-axis
                        linewidth=2,  # Line width
                        linecolor="black",  # Line color
                    ),
                    plot_bgcolor="white",  # Set background color to white
                )
                st.plotly_chart(fig)
                
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
                                    <td>{class_info["cname"]}{class_info["ccode"]}</td>
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
                                <tr>
                                    <td>Prerequisite count</td>
                                    <td>{class_info["prerequisite_classes"]}</td>
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

        
    with top_three_classes_offered_least_container:
        st.subheader("Top 3 classes offered the least")
        st.divider()
        response = requests.post("https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/least/classes")
        if response.status_code == 200:
                data = response.json()
                df = pd.json_normalize(data)
                df["normalized_class_count"] = (df["class_count"] - df["class_count"].min()) / (df["class_count"].max() - df["class_count"].min())
                
                if not df["normalized_class_count"].isna().any():
                    df["colors"] = generate_green_shades("#327136", df["normalized_class_count"])
                else:
                    df["colors"] = generate_green_shades("#327136", df["class_count"])

                fig = px.bar(
                    df, 
                    x="cid", 
                    y="class_count", 
                    color_discrete_sequence=df["colors"],
                    labels={"class_count": "Offered classes", "cid": "Class ID"},
                    )
                fig.update_traces(marker_color="#327136")
                
                fig.update_layout(
                    xaxis=dict(
                        type="category",
                        # categoryorder="total ascending",
                        showline=True,  # Show boundary line for x-axis
                        linewidth=2,  # Line width
                        linecolor="black",  # Line color
                        showgrid=True,  # Enable gridlines
                        gridcolor="lightgray",  # Gridline color
                        gridwidth=0.5,  # Gridline width
                    ),
                    yaxis=dict(
                        showline=True,  # Show boundary line for y-axis
                        linewidth=2,  # Line width
                        linecolor="black",  # Line color
                    ),
                    plot_bgcolor="white",  # Set background color to white
                )
                st.plotly_chart(fig)
                
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
                                <td>{class_info["cname"]}{class_info["ccode"]}</td>
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
                            <tr>
                                <td>Offered count</td>
                                <td>{class_info["class_count"]}</td>
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
        
    with total_sections_per_year_container:
        st.subheader("Total sections per year")
        st.divider()
        response = requests.post("https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/section/year")
        data = response.json()
        df = pd.json_normalize(data)
        df["normalized_sections"] = (df["sections"] - df["sections"].min()) / (df["sections"].max() - df["sections"].min()) 
        df["colors"] = generate_green_shades("#327136", df["normalized_sections"])

        fig = px.bar(
            df, 
            x="years", 
            y="sections", 
            color="years",
            color_discrete_sequence=df["colors"],
            labels={"sections": "Number of sections", "years": "Year"},
            )
        fig.update_layout(
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
        fig.add_trace(px.line(df, x="years", y="sections").data[0])
        st.plotly_chart(fig)

else:
    st.error("You need to login first to access this page.")