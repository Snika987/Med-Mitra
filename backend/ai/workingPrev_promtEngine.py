# backend/ai/prompt_engine.py

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

llm = ChatMistralAI(
    model="open-mistral-7b",
    temperature=0.3,
    api_key=os.getenv("MISTRAL_API_KEY")
)

template = """
You are a clinical assistant AI. Given the summary, lab results and an image caption,
generate a structured response in the following JSON format:

{{
  "soap": {{
    "subjective": "...",
    "objective": "...",
    "assessment": "...",
    "plan": "..."
  }},
  "diagnoses": ["..."],
  "investigations": ["..."],
  "treatment": ["..."],
  "confidence": "0.85"
}}

Summary: {summary}

Lab Results:
{lab}

Image Caption:
{image}
"""

prompt_template = ChatPromptTemplate.from_template(template)

def generate_clinical_response(summary, lab_data, image_caption):
    try:
        lab_str = "\n".join([
            f"- {lab['test_name']}: {lab['value']} {lab['unit']} (Note: {lab.get('note', '-')})"
            for lab in lab_data
        ])
        messages = prompt_template.format_messages(summary=summary, lab=lab_str, image=image_caption)
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return {"error": f"Prompt failed: {str(e)}"}
