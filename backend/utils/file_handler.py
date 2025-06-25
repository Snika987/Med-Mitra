import os
from uuid import uuid4
from fastapi import UploadFile

BASE_IMAGE_PATH = "backend/data/images/"
BASE_LAB_PATH = "backend/data/labs/"

os.makedirs(BASE_IMAGE_PATH, exist_ok=True)
os.makedirs(BASE_LAB_PATH, exist_ok=True)

def save_uploaded_file(file: UploadFile, file_type: str, case_id: str) -> str:
    ext = os.path.splitext(file.filename)[1]
    filename = f"{case_id}_{file.filename}"
    if file_type == "lab":
        path = os.path.join(BASE_LAB_PATH, filename)
    else:
        path = os.path.join(BASE_IMAGE_PATH, filename)

    with open(path, "wb") as f:
        f.write(file.file.read())
    return path
