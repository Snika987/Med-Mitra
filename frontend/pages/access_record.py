import streamlit as st
import requests

st.title("🔍 Access Patient Record")

patient_id = st.text_input("Enter Patient ID to retrieve case")

if st.button("Fetch Case"):
    if not patient_id:
        st.warning("Enter a patient ID.")
    else:
        response = requests.get(
            f"http://localhost:8000/get_case?patient_id={patient_id}"
        )

        if response.status_code == 200:
            result = response.json()
            st.success("Case retrieved!")
            st.json(result)
        else:
            st.error("Record not found or server error.")


