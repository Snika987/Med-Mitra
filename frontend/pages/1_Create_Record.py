import streamlit as st
import requests
import os
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from utils.deepgram_transcriber import transcribe_with_deepgram

st.set_page_config(page_title="Create Record", layout="centered")
st.title("Create Patient Record")

# ----------------- 🎙 Mic Recording Button ----------------- #
if "recording_path" not in st.session_state:
    st.session_state["recording_path"] = None

st.subheader("Optional: Record Summary via Microphone")
duration = st.slider("Recording duration (seconds)", 3, 60, 10)

if st.button("🎙 Record from Microphone"):
    try:
        fs = 16000  # Sample rate
        st.info("Recording... Speak now.")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        wav_path = os.path.join(tempfile.gettempdir(), "summary.wav")
        write(wav_path, fs, audio)
        st.session_state["recording_path"] = wav_path
        st.success("Recording complete.")
    except Exception as e:
        st.error(f"Recording failed: {str(e)}")

if st.session_state["recording_path"]:
    if st.button("📝 Transcribe Audio"):
        transcript = transcribe_with_deepgram(st.session_state["recording_path"])
        st.session_state["summary_text"] = transcript
        st.text_area("Transcribed Summary", value=transcript, height=100)

# ----------------- 📄 Patient Case Form ----------------- #

st.subheader("Fill Case Details")

summary = st.text_area("Enter case summary", value=st.session_state.get("summary_text", ""))
patient_id = st.text_input("Patient ID")
patient_name = st.text_input("Patient Name")

lab_file = st.file_uploader("Upload Lab Report (.csv or .pdf)", type=["csv", "pdf"])
image_file = st.file_uploader("Upload Radiology Image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if st.button("✅ Submit Case"):
    final_summary = summary or st.session_state.get("summary_text", "")
    if not final_summary or not patient_id or not patient_name:
        st.warning("Please complete all required fields.")
    else:
        files = {}
        if lab_file:
            files["lab_file"] = (lab_file.name, lab_file.getvalue(), lab_file.type)
        if image_file:
            files["image_file"] = (image_file.name, image_file.getvalue(), image_file.type)

        try:
            res = requests.post(
                "http://localhost:8000/submit_case/",
                data={
                    "summary": final_summary,
                    "patient_id": patient_id,
                    "patient_name": patient_name
                },
                files=files
            )
            if res.status_code == 200:
                st.success(f"✅ Case submitted successfully. Case ID: {res.json().get('case_id')}")
            else:
                st.error(f"Submission failed: {res.status_code}")
                st.text(res.text)
        except Exception as e:
            st.error(f"❌ Error submitting: {str(e)}")
