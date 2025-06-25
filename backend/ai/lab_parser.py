import os
import pandas as pd
import json
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()  # Loads your MISTRAL_API_KEY from .env

# Initialize Mistral LLM
llm = ChatMistralAI(
    model="open-mistral-7b",
    temperature=0.3,
    api_key=os.getenv("MISTRAL_API_KEY")
)

# Prompt template
template = """
You are a medical lab report assistant.

Given the following CSV table of lab results (which may be poorly formatted), extract and return a cleaned list of findings in raw JSON format.
Each item should include:
- "test_name"
- "value"
- "unit"
- "reference_range" (with "lower_limit" and "upper_limit" if available)
- "note" (use "-" if blank)

Respond ONLY with the raw JSON array. Do not include any explanation or markdown.

CSV Input:
{csv}
"""

prompt_template = ChatPromptTemplate.from_template(template)

def extract_lab_results(file_path: str):
    try:
        df = pd.read_csv(file_path, encoding='utf-8', engine='python', on_bad_lines='skip')
        csv_text = df.to_csv(index=False)
    except Exception as e:
        return [{"error": f"File reading failed: {str(e)}"}]

    try:
        prompt = prompt_template.format_messages(csv=csv_text)
        response = llm.invoke(prompt)
        raw_output = response.content.strip()

        # Attempt to parse JSON from the raw output
        if raw_output.startswith("```json"):
            raw_output = raw_output.strip("```json").strip("```").strip()
        elif raw_output.startswith("```"):
            raw_output = raw_output.strip("```").strip()

        return json.loads(raw_output)
    except Exception as e:
        return [{"error": f"Model output parse failed: {str(e)}"}]
