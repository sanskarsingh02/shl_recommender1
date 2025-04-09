# app/ai_recommend.py
import os
import requests
import csv
import io

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = os.getenv("GROQ_URL")

PROMPT_FILE = "prompts/assessment_prompt.txt"  # NEW

def load_prompt(job_description: str) -> str:
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            template = f.read()
        return template.format(job_description=job_description.strip())
    except Exception as e:
        raise RuntimeError(f"Failed to load prompt template: {e}")

def ai_recommend_assessments(job_description):
    prompt = load_prompt(job_description)  # 🧠 Externalized prompt

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a job analysis and SHL assessment recommender."},
            {"role": "user", "content": prompt}
        ]
    }

    print("🔁 Sending request to OpenRouter...")
    response = requests.post(GROQ_URL, headers=headers, json=data)
    response.raise_for_status()

    result_text = response.json()["choices"][0]["message"]["content"]

    print("✅ Groq/OpenRouter response received:")
    print("------ RESPONSE START ------")
    print(result_text[:500])
    print("------ RESPONSE END ------")

    # Save raw output for debugging
    with open("last_groq_output.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    # Clean up any markdown formatting
    result_text = result_text.strip()
    if result_text.startswith("```csv"):
        result_text = result_text.replace("```csv", "").strip()
    elif result_text.startswith("```CSV"):
        result_text = result_text.replace("```CSV", "").strip()
    if result_text.endswith("```"):
        result_text = result_text[:-3].strip()

    try:
        parsed = []
        reader = csv.DictReader(io.StringIO(result_text))
        for row in reader:
            if None not in row:  # skip malformed rows
                parsed.append(row)

        if parsed:
            print("✅ CSV parsed successfully with columns:", parsed[0].keys())
        else:
            print("⚠️ CSV parsed but no valid rows found.")

        return parsed
    except Exception as e:
        print("❌ CSV parsing failed:", str(e))
        raise
