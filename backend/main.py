from fastapi import FastAPI, UploadFile, Form, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from .db import SessionLocal, engine
from .models import Base, PatientCase
from .ai.lab_parser import extract_lab_results
from .utils.file_handler import save_uploaded_file  # optional if using file handler

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

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

    # Save files
    lab_path = image_path = None
    lab_results = None

    if lab_file:
        lab_path = f"backend/data/labs/{case_id}_{lab_file.filename}"
        with open(lab_path, "wb") as f:
            f.write(await lab_file.read())

        # Run lab parser on saved file
        lab_results = extract_lab_results(lab_path)

    if image_file:
        image_path = f"backend/data/images/{case_id}_{image_file.filename}"
        with open(image_path, "wb") as f:
            f.write(await image_file.read())

    # Save to DB
    case = PatientCase(
        case_id=case_id,
        patient_id=patient_id,
        patient_name=patient_name,
        summary=summary,
        lab_path=lab_path,
        image_path=image_path,
        lab_data=lab_results  # <-- save extracted lab info
    )
    db.add(case)
    db.commit()
    db.refresh(case)

    return {
        "message": "Case saved successfully",
        "case_id": case_id
    }
