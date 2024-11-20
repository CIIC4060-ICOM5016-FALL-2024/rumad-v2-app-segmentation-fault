import streamlit as st

st.title("Global Stats")

top_five_meetings_with_most_sections_container = st.container()
top_three_classes_as_prerequisite_container = st.container()
top_three_classes_offered_least_container = st.container()
total_sections_per_year_container = st.container()

with top_five_meetings_with_most_sections_container:
    st.subheader("Top 5 meetings with the most sections")
    graph = st.bar_chart(
        {"Meeting 1": 10, "Meeting 2": 8, "Meeting 3": 6, "Meeting 4": 4, "Meeting 5": 2}, 
        x_label="Number of sections",
        y_label="Meeting",
        horizontal=True, 
        use_container_width=True, 
        height=400, 
        color="#327136"
        )
    

with top_three_classes_as_prerequisite_container:
    st.subheader("Top 3 classes with the most prerequisites")
    graph = st.bar_chart(
        {"Class 1": 10, "Class 2": 8, "Class 3": 6}, 
        x_label="Number of prerequisites",
        y_label="Class",
        horizontal=True, 
        use_container_width=True, 
        height=400, 
        color="#327136"
        )
    
with top_three_classes_offered_least_container:
    st.subheader("Top 3 classes offered the least")
    graph = st.bar_chart(
        {"Class 1": 10, "Class 2": 8, "Class 3": 6}, 
        x_label="Number of times offered",
        y_label="Class",
        horizontal=True, 
        use_container_width=True, 
        height=400, 
        color="#327136"
        )
    
with total_sections_per_year_container:
    st.subheader("Total sections per year")
    graph = st.bar_chart(
        {"2019": 100, "2020": 80, "2021": 60}, 
        x_label="Number of sections",
        y_label="Year",
        horizontal=True, 
        use_container_width=True, 
        height=400, 
        color="#327136"
        )