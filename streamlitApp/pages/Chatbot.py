import json
import requests
import time
import streamlit as st

st.set_page_config(
    page_title="Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="./logos/university-of-puerto-rico-uprm-computer-science-and-engineering-college-png-favpng-M1JKJfqtXR77WLiF8x1j8U3cy.jpg"
)

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
            with st.chat_message(message["role"], avatar=message.get("avatar")):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Message"):
        # Display user message
        with st.chat_message("user", avatar="./logos/university-of-puerto-rico-uprm-computer-science-and-engineering-college-png-favpng-M1JKJfqtXR77WLiF8x1j8U3cy.jpg"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "./logos/university-of-puerto-rico-uprm-computer-science-and-engineering-college-png-favpng-M1JKJfqtXR77WLiF8x1j8U3cy.jpg"})

        # Loading spinner while waiting for a response
        with st.spinner("Processing..."):
            response = None
            try:
                # Send the API request
                response = requests.post(
                    "https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/chatbot",
                    json={"question": prompt, "context": st.session_state.context}
                )

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
        with st.chat_message("bot", avatar="./logos/Tarzan_7896.png"):
            st.markdown(answer)

        # Add bot's response to history
        st.session_state.messages.append({"role": "bot", "content": answer, "avatar": "./logos/Tarzan_7896.png"})
else:
    st.error("You need to login first to access this page.")
