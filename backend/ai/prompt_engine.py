import os
import json
import re
from dotenv import load_dotenv
from groq import Groq  # pip install groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(summary, lab_data, image_caption):
    return f"""
You are a clinical AI assistant.

Using this data, return structured clinical JSON (no markdown or explanations):

Summary: {summary}

Lab Results:
{json.dumps(lab_data, indent=2)}

Radiology Caption:
{image_caption}

Return JSON with:
- soap (subjective, objective, assessment, plan)
- diagnoses
- investigations
- treatment
- file_interpretations (lab_results, radiology)
- confidence (as string, 0.80–0.99)

ONLY return valid JSON.
"""

def extract_json(text):
    try:
        match = re.search(r"{.*}", text, re.DOTALL)
        if not match:
            return {"error": "No JSON found", "raw_output": text}
        return json.loads(match.group(0))
    except Exception as e:
        return {"error": f"JSON parse failed: {str(e)}", "raw_output": text}

def generate_clinical_response(summary, lab_data, image_caption):
    try:
        prompt = build_prompt(summary, lab_data, image_caption)
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # or llama3-70b-8192 if you want stronger",  # Or "llama3-8b-8192", etc.
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        text = response.choices[0].message.content
        return extract_json(text)
    except Exception as e:
        return {"error": f"Groq API call failed: {str(e)}"}
