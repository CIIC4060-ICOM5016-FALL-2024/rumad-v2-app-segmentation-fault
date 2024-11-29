import json
import requests
import time
import streamlit as st

st.title("Segmentation Fault Chat")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""
if "login" not in st.session_state:
    st.session_state.login = False  # Ensure login is initialized

if st.session_state.login:
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
                        # Send the API request
                        response = requests.post(
                            "https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/chatbot",
                            json={"question": prompt, "context": st.session_state.context}
                        )
                        if response.status_code == 200:  # Stop animation if response is ready
                            break

                # Process response
                if response and response.status_code == 200:
                    response_dict = response.json()
                    answer = response_dict.get("answer", "No answer provided.")
                    # Safely update context
                    st.session_state.context = response_dict.get("context", st.session_state.context)
                else:
                    answer = f"Error: {response.status_code} - {response.reason}"
            except requests.exceptions.RequestException as e:
                answer = f"Request failed: {e}"
            except json.JSONDecodeError:
                answer = "Failed to decode the server's response."
            except Exception as e:
                answer = f"An unexpected error occurred: {e}"

            # Display bot's response
            dots.empty()  # Remove loading animation
            st.markdown(answer)

        # Add bot's response to history
        st.session_state.messages.append({"role": "bot", "content": answer})
else:
    st.error("You need to login first to access this page.")
