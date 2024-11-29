import streamlit as st
import requests

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Authentication",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    .stButton>button {
        font-size: 16px;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
    }
    .stButton>button.login-btn {
        background-color: #007bff;
        color: white;
    }
    .stButton>button.login-btn:hover {
        background-color: #0056b3;
    }
    .stButton>button.logout-btn {
        background-color: #dc3545;
        color: white;
    }
    .stButton>button.logout-btn:hover {
        background-color: #c82333;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
        font-weight: bold;
    }
    .stForm label {
        font-size: 14px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "login" not in st.session_state:
    st.session_state['login'] = False

# Main function
def main():
    try:
        # Connect to the API
        response = requests.get("https://rumad-db-5dd7ab118ab8.herokuapp.com/")
        
        if response.status_code == 200:
            st.success("Connected to the API successfully!")

            # Use tabs for different login methods
            tabs = st.tabs(["Login", "Create new account"])

            # Tab for login
            with tabs[0]:
                st.markdown(
                    "<h2 style='color: #333;'>Login</h2>", 
                    unsafe_allow_html=True,
                )
                
                # Input fields for login form
                with st.form("login_form"):
                    username = st.text_input("Enter your username", placeholder="Username")
                    password = st.text_input("Enter your password", type="password", placeholder="Password")
                        
                    col_login, col_logout = st.columns([1, 8])
                    with col_login:
                        # Login button
                        login_button = st.form_submit_button("Login")
                    
                    with col_logout:
                        # Logout button
                        logout_button = st.form_submit_button("Logout", help="Log out of your account")

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
                                st.session_state['login'] = True
                            else:
                                st.error("Invalid username or password.")
                        else:
                            st.error("Please enter both username and password!")
                    
                    if logout_button:
                        st.session_state['login'] = False
                        st.success("You have been logged out successfully!")

            # Tab for creating new account
            with tabs[1]:
                st.markdown(
                    "<h2 style='color: #333;'>Create a New Account</h2>", 
                    unsafe_allow_html=True,
                )
                with st.form("register_form"):
                    new_username = st.text_input("Choose a username", placeholder="Username")
                    new_password = st.text_input("Choose a password", type="password", placeholder="Password")
                    register_button = st.form_submit_button("Register")
                    
                    if register_button:
                        if new_username and new_password:
                            # Call the API to create a new account
                            register_response = requests.post(
                                "https://rumad-db-5dd7ab118ab8.herokuapp.com/segmentation_fault/signup",
                                json={"username": new_username, "password": new_password},
                            )
                            if register_response.status_code == 201:
                                st.success("Account created successfully! Please log in.")
                            else:
                                st.error("Failed to create account. Try a different username.")
                        else:
                            st.error("Please enter both username and password!")

        else:
            st.error("Error: Unable to connect to the API. Please try again later.")
    except requests.exceptions.ConnectionError:
        st.error("Error: Could not connect to the API. Make sure the Flask API is running.")

# Run the app
if __name__ == "__main__":
    main()
