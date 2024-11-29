import json
import requests
import time
import streamlit as st

st.title("Segmentation Fault Chat")

# Initialize chat history and login state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""

if st.session_state.get("login"):
    with st.container():
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Message"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Loading animation while waiting for a response
        with st.chat_message("bot"):
            dots = st.empty()
            response = None
            try:
                for frame in ["", ".", "..", "..."]:
                    dots.markdown(f"Processing{frame}")
                    time.sleep(0.5)
                    if response is None:
                        response = requests.post(
                            "https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/chatbot",
                            json={"question": prompt, "context": st.session_state.context}
                        )
                        if response.ok:
                            break
                # Parse response
                response_dict = response.json()
                answer = response_dict.get("answer", "No answer provided.")
            except Exception as e:
                answer = f"An error occurred: {e}"

            # Display bot's response
            dots.empty()  # Remove loading animation
            st.markdown(answer)

        # Add bot's response to history
        st.session_state.messages.append({"role": "bot", "content": answer})
        st.session_state.context = response_dict.get("context", "")
else:
    st.error("You need to login first to access this page.")
