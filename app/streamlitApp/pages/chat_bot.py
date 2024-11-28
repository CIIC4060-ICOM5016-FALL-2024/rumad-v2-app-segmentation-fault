import json
import streamlit as st
import sys
import os
import time

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

        # Display loading animation in chat message container
        with st.chat_message("bot"):
            dots = st.empty()  # Placeholder for the loading animation
            for _ in range(10):  # Animation loop for 3 seconds
                for frame in ["", ".", "..", "..."]:
                    dots.markdown(f"Processing{frame}")
                    time.sleep(0.5)

            # Send the user's question to the chatbot function
            try:
                response_json = chatbot(prompt)  # This returns a JSON string
                response_dict = json.loads(response_json)  # Convert JSON string to dictionary
                answer = response_dict.get("answer", "No answer provided.")  # Safely get the "answer"
            except json.JSONDecodeError as e:
                answer = f"JSON decode error: {e}"
            except Exception as e:
                answer = f"An unexpected error occurred: {e}"

            # Update the bot's response after processing
            dots.markdown(answer)

        # Add chatbot's response to chat history
        st.session_state.messages.append({"role": "bot", "content": answer})

else:
    st.error("You need to login first to access this page.")
