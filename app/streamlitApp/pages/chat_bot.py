import json
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from app.vectorDB.chatBot.chat import chatbot 

st.title("Segmentation Fault Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.get("login"):
    with st.container():
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Message"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Send the user's question to the chatbot function
        try:
            response_json = chatbot(prompt)  # This returns a JSON string
            print(response_json)
            response_dict = json.loads(response_json)  # Convert JSON string to dictionary
            answer = response_dict.get("answer", "No answer provided.")  # Safely get the "answer"
        except json.JSONDecodeError as e:
            answer = f"JSON decode error: {e}"
        except Exception as e:
            answer = f"An unexpected error occurred: {e}"

        # Display the chatbot's response in chat message container
        with st.chat_message("bot"):
            st.markdown(answer)
        # Add chatbot's response to chat history
        st.session_state.messages.append({"role": "bot", "content": answer})


else:
    st.error("You need to login first to access this page.")