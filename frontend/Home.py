import streamlit as st

st.set_page_config(page_title="Med Assistant", page_icon="🩺")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

st.title("🩺 Med Assistant")

if not st.session_state["authenticated"]:
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid credentials")
else:
    st.success("Welcome! Use the sidebar to navigate between pages.")
