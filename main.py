# main.py
import streamlit as st
import requests
from app.utils import extract_job_description_from_url

FLASK_URL = "http://localhost:5000"

st.set_page_config(page_title="SHL Recommender", layout="centered")

# 🌸 Light styling
st.markdown("""
    <style>
    body {
        background-color: #ffe6f0;
    }
    .stApp {
        background-color: #ffe6f0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 SHL Recommender & Assessment Generator")

# 🔁 Updated job description input block (manual or URL)
st.header("📋 Job Description Input (Manual or URL)")
input_mode = st.radio("Choose input type:", ["Paste Manually", "Use Job Description URL"], horizontal=True)

job_desc = ""

if input_mode == "Paste Manually":
    job_desc = st.text_area("Enter full job description here")
else:
    job_url = st.text_input("Paste job description URL")
    if job_url:
        with st.spinner("🔍 Extracting job description from URL..."):
            job_desc = extract_job_description_from_url(job_url)
        st.success("✅ Extracted job description:")
        st.text_area("Preview:", job_desc, height=200)

if st.button("🔮 Get AI Recommendations"):
    if not job_desc.strip():
        st.warning("Please provide a job description.")
    else:
        with st.spinner("Asking Groq AI for recommendations..."):
            try:
                res = requests.post(f"{FLASK_URL}/recommend", json={"query": job_desc})
                res.raise_for_status()
                data = res.json()
                recommendations = data.get("recommended_assessments", [])

                if not recommendations:
                    st.warning("⚠️ No recommendations returned by Groq.")
                else:
                    st.success("✅ AI-based recommendations ready!")
                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"### {i}. Assessment Recommendation")
                        st.write(f"**Description**: {rec.get('description', 'N/A')}")
                        st.write(f"**Type**: {', '.join(rec.get('test_type', ['N/A']))}")
                        st.write(f"**Duration**: {rec.get('duration', 'N/A')} mins")
                        st.write(f"**Remote Testing**: {rec.get('remote_support', 'N/A')}")
                        st.write(f"**Adaptive Support**: {rec.get('adaptive_support', 'N/A')}")
                        st.write(f"[🔗 View Assessment]({rec.get('url', '#')})")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")

st.divider()

# ✅ Original skill-based recommender block (unchanged)
st.header("🛠️ Manual Skill-Based Recommendation")
with st.form("input_form"):
    skills_input = st.text_input("Enter skills (comma-separated):", "")
    submitted = st.form_submit_button("Get Recommendations")

if submitted and skills_input:
    skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]

    with st.spinner("Fetching keyword-based recommendations..."):
        try:
            res = requests.post(f"{FLASK_URL}/recommend", json={"skills": skills_list})
            res.raise_for_status()
            data = res.json()
            recommendations = data.get("recommendations", [])

            if not recommendations:
                st.warning("⚠️ No matching assessments found.")
            else:
                st.success("✅ Recommendations retrieved!")
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"### {i}. {rec.get('Assessment Name', 'N/A')}")
                    st.write(f"**Type**: {rec.get('Test Type', 'N/A')}")
                    st.write(f"**Duration**: {rec.get('Duration', 'N/A')}")
                    st.write(f"**Skills**: {rec.get('Skills', 'N/A')}")
                    st.write(f"[🔗 Visit]({rec.get('URL', '#')})")

                    if st.button(f"Generate Assessment for '{rec.get('Assessment Name', '')}'", key=f"gen_{i}"):
                        with st.spinner("Generating assessment via Groq API..."):
                            prompt = f"Generate a detailed SHL assessment for: {rec.get('Assessment Name', '')}."
                            gen_res = requests.post(f"{FLASK_URL}/generate_assessment", json={"prompt": prompt})

                            try:
                                gen_data = gen_res.json()
                                if gen_res.status_code == 200:
                                    st.subheader("📋 SHL Assessment")
                                    st.markdown(gen_data.get("assessment", "No response."))
                                else:
                                    st.error(gen_data.get("error", "❌ Generation failed."))
                            except Exception as e:
                                st.error(f"❌ Error reading response: {e}")
        except Exception as e:
            st.error(f"Request failed: {e}")
