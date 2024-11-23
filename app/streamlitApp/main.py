import streamlit as st
import requests

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Authentication",
    layout="centered",
)

# Title
st.title("Aunthetication Page")

# Main function
def main():
    try:
        # Connect to the API
        response = requests.get("https://rumad-db-5dd7ab118ab8.herokuapp.com/")
        
        if response.status_code == 200:
            st.success("Connected to the API successfully!")

            # Authentication UI
            st.title("🔒 Authentication")

            # Tabs for different login methods
            auth_mode = st.radio(
                "Choose an option:",
                ["Create new account", "Login to existing account"],
                index=1,
                horizontal=True,
            )

            # Form for login
            if auth_mode == "Login to existing account":
                st.subheader("Login to existing account")
                
                # Input fields for login form
                with st.form("login_form"):
                    username = st.text_input("Enter your unique username", placeholder="Username")
                    password = st.text_input("Enter your password", type="password", placeholder="Password")
                    show_password = st.checkbox("Show password")
                    
                    # Display the password dynamically if checkbox is selected
                    if show_password:
                        st.text(f"Password: {password}")

                    # Login button
                    login_button = st.form_submit_button("🔓 Login")

                    # Handle login logic
                    if login_button:
                        if username and password:
                            # Call the API for authentication 
                            login_response = requests.post(
                                "https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/login",
                                json={"username": username, "password": password},
                            )
                            
                            if login_response.status_code == 200:
                                st.success(f"Welcome back, {username}!")
                            else:
                                st.error("Invalid username or password.")
                        else:
                            st.error("Please enter both username and password!")

            # Optional: UI for "Create new account" 
            elif auth_mode == "Create new account":
                st.subheader("Create new account")
                with st.form("register_form"):
                    new_username = st.text_input("Choose a unique username", placeholder="Username")
                    new_password = st.text_input("Choose a password", type="password", placeholder="Password")
                    register_button = st.form_submit_button("Register")
                    
                    if register_button:
                        # Call the API to create a new account
                        register_response = requests.post(
                            "https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/signup",
                            json={"username": new_username, "password": new_password},
                        )
                        print(register_response.status_code)
                        if register_response.status_code == 201:
                            st.success("Account created successfully! Please log in.")
                        else:
                            st.error("Failed to create account. Try a different username.")

        else:
            st.error("Error: Unable to connect to the API. Please try again later.")
    except requests.exceptions.ConnectionError:
        st.error("Error: Could not connect to the API. Make sure the Flask API is running.")

# Run the app
if __name__ == "__main__":
    main()
