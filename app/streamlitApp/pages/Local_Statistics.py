import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from matplotlib import colors as mcolors
import json

# inyect CSS to style the page
st.markdown(
    """
    <style>
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        border-radius: 10px;
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

with top_three_rooms_per_capacity_container:
    st.subheader("Top 3 rooms with the most capacity")
    building = "Stefani"
    buildings = ["Stefani", "Software", "Monzon"]
    for i, col in enumerate(st.columns(3)):
        with col:
            if st.button(buildings[i]):
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
                y="room_number",
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
                    showline=True,  # Show boundary line for y-axis
                    linewidth=2,  # Line width
                    linecolor="black",  # Line color
                    showgrid=True,  # Enable gridlines
                    gridcolor="lightgray",  # Gridline color
                    gridwidth=0.5,  # Gridline width
                ),
                plot_bgcolor="white",  # Set background color to white
            )
            st.plotly_chart(fig_stacked)
        else:
            st.write("Error: " + response.status_code)
    except:
        st.write("Error: Could not connect to the API.")



                

with top_three_rooms_per_ration_container:
    st.subheader("Top 3 rooms with the most student-to-capacity ratio")
    graph = st.bar_chart(
        {"Room 1": 10, "Room 2": 8, "Room 3": 6}, 
        x_label="Ratio",
        y_label="Room",
        horizontal=True, 
        use_container_width=True, 
        height=400, color="#327136"
        )

with top_three_classes_taught_per_semester_container:
    st.subheader("Top 3 most taught classes per semester.")
    graph = st.bar_chart(
        {"Class 1": 10, "Class 2": 8, "Class 3": 6}, 
        x_label="Number of times taught",
        y_label="Class",
        horizontal=True, 
        use_container_width=True, 
        height=400, 
        color="#327136"
        )

with top_three_classes_taught_per_room_container:
    st.subheader("Top 3 classes that were taught the most per room")
    graph = st.bar_chart(
        {"Class 1": 10, "Class 2": 8, "Class 3": 6}, 
        x_label="Number of times taught",
        y_label="Class",
        horizontal=True, 
        use_container_width=True, 
        height=400, 
        color="#327136")

