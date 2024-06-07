# login.py
import streamlit as st
from time import sleep


def login():
    st.title("Chào mừng bạn đến với CRM LƯU THÙY")
    st.write("Xin vui lòng đăng nhập để sử dụng.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in", type="primary"):
        if username == st.secrets["login"]["username2"] and password == st.secrets["login"]["password2"]:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            sleep(0.5)
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password")

@st.cache_data(allow_output_mutation=True)
def get_logged_in():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in

def show_login():
    if not get_logged_in():
        login()