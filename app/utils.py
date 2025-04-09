# app/utils.py
import requests
from bs4 import BeautifulSoup

def extract_job_description_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        # Remove unwanted tags
        for script in soup(["script", "style", "noscript"]):
            script.decompose()

        # Get visible text
        text = soup.get_text(separator=" ", strip=True)
        lines = [line for line in text.splitlines() if len(line.strip()) > 60]
        job_text = " ".join(lines[:15])  # Limit to first 15 useful lines
        return job_text
    except Exception as e:
        return f"⚠️ Failed to extract content from URL: {e}"
