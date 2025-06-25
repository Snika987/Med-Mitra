from prompt_engine import generate_clinical_response
import json

summary = "Patient is a 54-year-old male with fatigue and shortness of breath."
lab_data = [
    {
        "test_name": "Hemoglobin",
        "value": "13.2",
        "unit": "g/dl",
        "reference_range": {
            "lower_limit": "12",
            "upper_limit": "16"
        },
        "note": "-"
    },
    {
        "test_name": "WBC",
        "value": "6.2",
        "unit": "x10^3/uL",
        "reference_range": {
            "lower_limit": "4",
            "upper_limit": "11"
        },
        "note": "Normal"
    }
]
image_caption = "Chest X-ray shows mild cardiomegaly with no pleural effusion."

result = generate_clinical_response(summary, lab_data, image_caption)

print("\n--- 🧠 AI Clinical Output ---\n")
print(json.dumps(result, indent=2))
