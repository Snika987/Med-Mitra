# Med-Mitra: Multimodal Clinical Insight Assistant

**Med-Mitra** is an AI-powered clinical assistant designed for healthcare professionals to rapidly analyze patient cases by combining:
- Case summaries (typed or dictated)
- Lab reports (CSV/PDF)
- Radiology images (JPG/PNG)

It uses multimodal reasoning to return structured clinical insights in the SOAP format, along with differential diagnoses, treatment suggestions, per-file interpretations, and a confidence score.

---

## 🧠 Project Highlights

- **Multimodal Fusion**: Combines text, lab results, and radiology for holistic AI interpretation
- **Voice Support**: Real-time voice-to-text using Deepgram
- **Image Captioning**: AI captions radiology images with BLIP
- **Structured Output**: SOAP note, diagnoses, treatment, and interpretation
- **PDF Export**: Generate downloadable case summaries
- **Fast Interface**: Lightweight and responsive Streamlit frontend

---

## 🔄 App Flow

### 1. Web UI (Streamlit)
Doctors can:
- Enter case summaries (voice or text)
- Upload lab reports and radiology images
- Retrieve old cases using Case ID or Patient ID

### 2. Backend (FastAPI)
- Receives uploads, parses data
- Stores metadata in a local database
- Calls the AI engine and returns structured insights

### 3. AI Engine (LLMs + Captioning)
- Lab Parser: Extracts structured fields from CSV/PDF
- Image Captioner: Describes chest X-rays using BLIP
- LLM (via Groq): Synthesizes SOAP + diagnoses + treatment plan

---

## 🤖 Models & Tech Used

| Component           | Tool / Model                             | Reason for Use                                           |
|---------------------|------------------------------------------|----------------------------------------------------------|
| **LLM**             | `llama3-8b-8192` (Groq API)              | Fast, powerful open model for clinical reasoning         |
| **Image Captioning**| `Salesforce/blip-image-captioning-base` | Lightweight caption generator for X-rays                 |
| **Lab Parsing**     | Custom logic with Pandas + Regex         | Extracts structured test data from CSV/PDF               |
| **Speech-to-Text**  | Deepgram SDK (v3)                        | Real-time microphone dictation for summaries             |

---

## 🔐 API Keys Required

1. **Groq API Key** – For using LLaMA 3 models  
   Sign up at: https://console.groq.com

2. **Deepgram API Key** – For voice input transcription  
   Get yours at: https://console.deepgram.com

Set both keys in your `.env` file:

```env
GROQ_API_KEY=your-groq-key
DEEPGRAM_API_KEY=your-deepgram-key
