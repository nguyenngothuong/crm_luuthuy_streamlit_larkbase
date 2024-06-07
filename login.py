# login.py
import streamlit as st
from time import sleep

def login():
    st.title("Welcome to Diamond Corp")

    st.write("Please log in to continue.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in", type="primary"):
        if username == st.secrets["login"]["username2"] and password == st.secrets["login"]["password2"]:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            sleep(0.5)
            return True
        else:
            st.error("Incorrect username or password")
            return False