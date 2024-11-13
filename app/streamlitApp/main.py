import streamlit as st
import requests

st.set_page_config(
    page_title="This is the Streamlit frontend of Segmentation Fault team."
)

st.title('This is the RestAPI of Segmentation Fault team.')

def main():
    try:
        response = requests.get("https://rumad-db-5dd7ab118ab8.herokuapp.com/")
        if response.status_code == 200:
            st.write("Home for the Segmentation Fault team.")
        else:
            st.write("Error:")
    except requests.exceptions.ConnectionError:
        st.write("Error: Could not connect to the API. Make sure the Flask API is running.")

if __name__ == "__main__":
    main()
