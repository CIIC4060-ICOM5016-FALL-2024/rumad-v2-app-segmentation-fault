import streamlit as st

st.title("Local Stats")

top_three_rooms_per_capacity_container = st.container()
top_three_rooms_per_ration_container = st.container()
top_three_classes_taught_per_semester_container = st.container()
top_three_classes_taught_per_room_container = st.container()

with top_three_rooms_per_capacity_container:
    st.subheader("Top 3 rooms with the most capacity")
    graph = st.bar_chart(
        {"Room 1": 100, "Room 2": 80, "Room 3": 60}, 
        x_label="Capacity",
        y_label="Room",
        horizontal=True, 
        use_container_width=True, 
        height=400, 
        color="#327136"
        )

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

