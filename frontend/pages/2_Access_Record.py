import streamlit as st
import requests
from utils.pdf_exporter import generate_pdf

st.set_page_config(page_title="Access Record", layout="wide")
st.title("Access Patient Case")

with st.sidebar:
    st.markdown("## Navigation")
    st.page_link("Home.py", label="Home")
    st.page_link("pages/1_Create_Record.py", label="Create Patient Record")
    st.page_link("pages/2_Access_Record.py", label="Access Patient Record", disabled=True)

st.markdown("---")

# Input for ID
col1, col2 = st.columns([3, 1])
with col1:
    identifier = st.text_input("Enter Patient ID or Case ID")
with col2:
    search_type = st.selectbox("Search by", ["patient_id", "case_id"])

# Fetch
if st.button("Fetch Case"):
    if not identifier:
        st.warning("Please enter an ID.")
    else:
        try:
            url = f"http://localhost:8000/get_case?{search_type}={identifier}"
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()

                # Display summary
                with st.expander("📝 Patient Overview", expanded=True):
                    st.markdown(f"**Patient Name:** {result['patient_name']}")
                    st.markdown(f"**Patient ID:** {result['patient_id']}")
                    st.markdown(f"**Case ID:** {result['case_id']}")
                    st.markdown(f"**Summary:** {result['summary']}")
                    st.markdown(f"**Confidence:** {result.get('confidence', 'N/A')}")

                # Display SOAP Note
                if result.get("soap"):
                    with st.expander("📄 SOAP Note", expanded=True):
                        for key, val in result['soap'].items():
                            st.markdown(f"**{key.capitalize()}:** {val}")

                # Display Diagnoses
                if result.get("diagnoses"):
                    with st.expander("🧠 Diagnoses"):
                        for diag in result['diagnoses']:
                            st.markdown(f"- {diag}")

                # Display Investigations
                if result.get("investigations"):
                    with st.expander("🔬 Investigations"):
                        for item in result['investigations']:
                            st.markdown(f"- {item}")

                # Display Treatment
                if result.get("treatment"):
                    with st.expander("💊 Treatment Plan"):
                        for step in result['treatment']:
                            st.markdown(f"- {step}")

                # Display Interpretations
                if result.get("interpretations"):
                    with st.expander("📂 File Interpretations"):
                        interp = result['interpretations']
                        if interp.get("lab_results"):
                            st.markdown("**Lab Results:**")
                            for lab in interp['lab_results']:
                                st.markdown(
                                    f"- {lab['test_name']}: {lab['value']} {lab.get('unit', '')} ({lab.get('note', '')})"
                                )
                        if interp.get("radiology"):
                            st.markdown("**Radiology:**")
                            st.markdown(f"{interp['radiology']}")

                # PDF export button
                pdf_bytes = generate_pdf(result)
                st.download_button(
                    label="📥 Download as PDF",
                    data=pdf_bytes,
                    file_name=f"case_{result['case_id']}.pdf",
                    mime="application/pdf"
                )

                # Feedback
                st.markdown("---")
                st.markdown("#### Was this information helpful?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Yes"):
                        st.success("Thanks for your feedback!")
                with col2:
                    if st.button("👎 No"):
                        st.warning("We'll work on improving it.")

            else:
                st.error("Error fetching record. Please check the ID and try again.")
        except Exception as e:
            st.error(f"Server error: {str(e)}")
