Med-Mitra: Multimodal Clinical Insight Assistant
Med-Mitra is an AI-powered clinical assistant designed for healthcare professionals to rapidly analyze patient cases by combining:

Case summaries (typed or dictated)
Lab reports (CSV/PDF)
Radiology images (JPG/PNG)

It uses multimodal reasoning to return structured clinical insights in the SOAP format, along with differential diagnoses, treatment suggestions, per-file interpretations, and a confidence score.
🧠 Project Highlights

Multimodal Fusion: Combines text, lab results, and radiology for holistic AI interpretation
Voice Support: Real-time voice-to-text using Deepgram
Image Captioning: AI captions radiology images with BLIP
Structured Output: SOAP note, diagnoses, treatment, and interpretation
PDF Export: Generate downloadable case summaries
Fast Interface: Lightweight and responsive Streamlit frontend

🔄 App Flow
1. Web UI (Streamlit)
Doctors can:

Enter case summaries (voice or text)
Upload lab reports and radiology images
Retrieve old cases using Case ID or Patient ID

2. Backend (FastAPI)

Receives uploads, parses data
Stores metadata in a local database
Calls the AI engine and returns structured insights

3. AI Engine (LLMs + Captioning)

Lab Parser: Extracts structured fields from CSV/PDF
Image Captioner: Describes chest X-rays using BLIP
LLM (via Groq): Synthesizes SOAP + diagnoses + treatment plan

🤖 Models & Tech Used



Component
Tool / Model
Reason for Use



LLM
llama3-8b-8192 (Groq API)
Fast, powerful open model for clinical reasoning


Image Captioning
Salesforce/blip-image-captioning-base
Lightweight caption generator for X-rays


Lab Parsing
Custom logic with Pandas + Regex
Extracts structured test data from CSV/PDF


Speech-to-Text
Deepgram SDK (v3)
Real-time microphone dictation for summaries


🔐 API Keys Required

Groq API Key – For using LLaMA 3 modelsSign up at: https://console.groq.com

Deepgram API Key – For voice input transcriptionGet yours at: https://console.deepgram.com


Set both keys in your .env file:
GROQ_API_KEY=your-groq-key
DEEPGRAM_API_KEY=your-deepgram-key

📉 Limitations & Challenges



Area
Challenge / Limitation



Image Captioning
BLIP is not fine-tuned for medical radiology (e.g., chest X-rays, MRIs)


PDF Parsing
Lab PDFs vary greatly — some may not extract cleanly


Speech Input
Real-time transcription depends on browser & mic hardware, may timeout on long dictation


Model Generalization
LLMs may hallucinate slightly or produce incomplete SOAP outputs in rare cases


Free-tier API Limits
Groq/Deepgram free plans may limit daily usage


🚀 Setup and Installation
Prerequisites

Python 3.11+
Docker (optional, for containerized deployment)
Git
API keys for Groq and Deepgram

Local Setup

Clone the Repository:
git clone https://github.com/your-username/med-mitra.git
cd med-mitra


Create and Activate Virtual Environment:
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Environment Variables:Create a .env file in the project root and add:
GROQ_API_KEY=your-groq-key
DEEPGRAM_API_KEY=your-deepgram-key


Run the Application:

Start the FastAPI backend:uvicorn backend.main:app --host 0.0.0.0 --port 8000


In a separate terminal, start the Streamlit frontend:streamlit run frontend/Home.py --server.port 8501


Access the frontend at http://localhost:8501 and the API at http://localhost:8000.



Docker Setup

Build and Run with Docker:
docker build -t med-mitra .
docker run -p 8000:8000 -p 8501:8501 --env-file .env med-mitra


Access the frontend at http://localhost:8501 and the API at http://localhost:8000.


Using Docker Compose (recommended for multi-service setup):
docker-compose up --build


This starts both FastAPI and Streamlit services, plus a PostgreSQL database if configured.



🗂 Sample Dataset

Location: data/ folder
Contents:
data/labs/*.csv and *.pdf: Sample lab reports (e.g., blood tests, lung reports).
data/images/*.jpg and *.png: Sample radiology images (e.g., chest X-rays, MRIs).


Usage:
Upload these files via the Streamlit UI (http://localhost:8501) to test case creation.
Use Case ID or Patient ID to retrieve stored cases.



📝 Usage

Create a Case:

Navigate to the "Create Record" page in the Streamlit UI.
Enter a case summary (type or use voice input via Deepgram).
Upload lab reports (CSV/PDF) and radiology images (JPG/PNG).
Submit to receive a structured SOAP note, diagnoses, and treatment plan.


Access Past Cases:

Go to the "Access Record" page.
Search by Case ID or Patient ID to view previous case details.


Export to PDF:

Download case summaries as PDFs from the UI.



📚 Notes

Ensure API keys are set correctly to avoid authentication errors.
Large image/lab files may slow down uploads; optimize files if needed.
The sample dataset is for testing purposes only and contains anonymized data.
