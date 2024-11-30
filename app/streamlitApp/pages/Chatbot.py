import json
import streamlit as st
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from app.vectorDB.chatBot.chat import chatbot 

st.set_page_config(
    page_title="Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="./logos/seal-rum-uprm-1280x1280px.png"
)

st.title("Segmentation Fault Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def maintain_message_history():
    while len(st.session_state.messages) > 6:  # 3 interactions = 6 messages (3 user + 3 bot)
        st.session_state.messages.pop(0)

if st.session_state.get("login"):
    with st.container():
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message.get("avatar")):
                st.markdown(message["content"])


    # Accept user input
    if prompt := st.chat_input("Message"):


        # Display user message in chat message container
        with st.chat_message("user", avatar="./logos/seal-rum-uprm-1280x1280px.png"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "./logos/seal-rum-uprm-1280x1280px.png"})

        # maintain_message_history()
        with st.spinner("Processing..."):
            response = None
            try:
                response = chatbot(prompt, json.dumps(st.session_state.messages))

                if response:
                    response_dict = json.loads(response[0])
                    answer = response_dict.get("answer", "No answer provided.")

                else:
                    answer = "No answer provided."
            except json.JSONDecodeError as e:
                answer = f"JSON decode error: {e}"

        with st.chat_message("bot", avatar="./logos/Tarzan_7896.png"):
            st.markdown(answer)

        st.session_state.messages.append({"role": "bot", "content": answer, "avatar": "./logos/Tarzan_7896.png"})


        # Display loading animation in chat message container
        # with st.chat_message("bot"):
        #     dots = st.empty()  # Placeholder for the loading animation
        #     for _ in range(10):  # Animation loop for 3 seconds
        #         for frame in ["", ".", "..", "..."]:
        #             dots.markdown(f"Processing{frame}")
        #             time.sleep(0.5)

        #     # Send the user's question to the chatbot function
        #     try:
               
        #         response_json = chatbot(prompt, json.dumps(st.session_state.messages))  # This returns a JSON string
    
        #         response_dict = json.loads(response_json[0])  # Convert JSON string to dictionary
        #         answer = response_dict.get("answer", "No answer provided.")  # Safely get the "answer"
        #     except json.JSONDecodeError as e:
        #         answer = f"JSON decode error: {e}"
        #     except Exception as e:
        #         answer = f"An unexpected error occurred: {e}"

        #     # Update the bot's response after processing
        #     dots.markdown(answer)

        # # Add chatbot's response to chat history
        # st.session_state.messages.append({"role": "bot", "content": answer})
        # maintain_message_history()

else:
    st.error("You need to login first to access this page.")
