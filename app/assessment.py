# app/assessment.py
import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/v1/chat/completions"

def generate_shl_assessment(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are an SHL assessment generator."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(GROQ_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def fetch_catalog_structure():
    prompt = (
        "Please extract SHL assessments from https://www.shl.com/en/assessments/ "
        "and format them into CSV with the following headers:\n"
        "- Assessment Name\n"
        "- Description (must include keywords, competencies, or skills covered)\n"
        "- Duration\n"
        "- URL\n"
        "- Test Type (e.g., Cognitive, Personality, Coding)\n"
        "- Remote Testing Support (Yes/No)\n"
        "- Adaptive/IRT Support (Yes/No)\n\n"
        "Make sure to include descriptions rich in searchable skills or traits. Return only valid CSV format, no markdown, no commentary."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a data assistant that extracts structured tabular data from content."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(GROQ_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def save_catalog_to_csv():
    csv_data = fetch_catalog_structure()
    
    # 👇 Print the first part to debug
    print("=== Groq CSV preview ===")
    print(csv_data[:500])  # Print first 500 chars of Groq's response

    filepath = "data/shl_dataset.csv"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(csv_data)
    return filepath
