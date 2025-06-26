from fastapi import FastAPI, UploadFile, Form, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import uuid4
import os

from .db import SessionLocal, engine
from .models import Base, PatientCase
from .ai.lab_parser import extract_lab_results
from .ai.image_caption import generate_image_caption
from .ai.prompt_engine import generate_clinical_response

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit_case/")
async def submit_case(
    summary: str = Form(...),
    patient_id: str = Form(...),
    patient_name: str = Form(...),
    lab_file: UploadFile = File(None),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    case_id = str(uuid4())
    lab_path = image_path = None
    lab_results = image_caption = None

    # Save and parse lab file
    if lab_file:
        lab_path = f"backend/data/labs/{case_id}_{lab_file.filename}"
        with open(lab_path, "wb") as f:
            f.write(await lab_file.read())
        # Only parse if CSV
        if lab_file.filename.endswith(".csv"):
            lab_results = extract_lab_results(lab_path)

    # Save and caption image
    if image_file:
        image_path = f"backend/data/images/{case_id}_{image_file.filename}"
        with open(image_path, "wb") as f:
            f.write(await image_file.read())
        image_caption = generate_image_caption(image_path)
    else:
        image_caption = "No radiology image provided."

    # Generate AI clinical response
    ai_output = generate_clinical_response(
        summary=summary,
        lab_data=lab_results or [],
        image_caption=image_caption
    )

    # Save case to DB
    case = PatientCase(
        case_id=case_id,
        patient_id=patient_id,
        patient_name=patient_name,
        summary=summary,
        lab_path=lab_path,
        image_path=image_path,
        lab_data=lab_results,
        soap=ai_output.get("soap"),
        diagnoses=ai_output.get("diagnoses"),
        treatment=ai_output.get("treatment"),
        interpretations=ai_output.get("file_interpretations"),
        confidence=ai_output.get("confidence")
    )
    db.add(case)
    db.commit()
    db.refresh(case)

    return {
        "message": "✅ Case saved and processed successfully!",
        "case_id": case_id,
        "ai_summary": ai_output
    }

@app.get("/get_case/")
def get_case(case_id: str = None, patient_id: str = None, db: Session = Depends(get_db)):
    if not case_id and not patient_id:
        raise HTTPException(status_code=400, detail="Provide either case_id or patient_id.")

    query = db.query(PatientCase)
    case = None

    if case_id:
        case = query.filter(PatientCase.case_id == case_id).first()
    elif patient_id:
        case = query.filter(PatientCase.patient_id == patient_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    return {
        "case_id": case.case_id,
        "patient_id": case.patient_id,
        "patient_name": case.patient_name,
        "summary": case.summary,
        "lab_data": case.lab_data,
        "image_path": case.image_path,
        "soap": case.soap,
        "diagnoses": case.diagnoses,
        "treatment": case.treatment,
        "interpretations": case.interpretations,
        "confidence": case.confidence
    }
