import streamlit as st
import requests

st.title("📄 Create Patient Record")

summary = st.text_area("Enter case summary")
patient_id = st.text_input("Patient ID")
patient_name = st.text_input("Patient Name")

lab_file = st.file_uploader("Upload Lab Report (.csv)", type=["csv"])
image_file = st.file_uploader("Upload Radiology Image", type=["jpg", "png"])



if st.button("Submit Case"):
    if not summary or not patient_id or not patient_name:
        st.error("Please fill in all fields")
    else:
        files = {}
        if lab_file:
            files["lab_file"] = (lab_file.name, lab_file.getvalue())
        if image_file:
            files["image_file"] = (
                image_file.name,
                image_file.getvalue(),
                "image/jpeg" if image_file.type == "image/jpeg" else "image/png"
            )


        response = requests.post(
            "http://localhost:8000/submit_case/",
            data={
                "summary": summary,
                "patient_id": patient_id,
                "patient_name": patient_name,
            },
            files=files
        )

        if response.status_code == 200:
            result = response.json()
            st.success("Case submitted successfully!")
            st.json(result)
        else:
            st.error(f"Error: {response.status_code}")
            st.text(response.text)
