# app/api.py
from flask import request, jsonify
from app import app
from app.ai_recommend import ai_recommend_assessments


# ✅ Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


# ✅ Required recommendation endpoint (query -> LLM)
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Missing required field: 'query'"}), 400

    try:
        assessments = ai_recommend_assessments(query)

        # 🔁 Format result to match assessor expectations
        formatted = []
        for item in assessments[:10]:  # Limit to max 10
            formatted.append({
                "url": item.get("URL", "").strip(),
                "adaptive_support": item.get("Adaptive/IRT Support", "No").strip(),
                "description": item.get("Skills Assessed", "").strip(),
                "duration": extract_duration(item.get("Duration", "")),
                "remote_support": item.get("Remote Testing Support", "No").strip(),
                "test_type": [item.get("Test Type", "").strip()]
            })

        return jsonify({"recommended_assessments": formatted}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Helper to extract integer duration from "30 mins" etc.
def extract_duration(duration_str):
    try:
        if isinstance(duration_str, str) and "min" in duration_str.lower():
            return int(''.join(filter(str.isdigit, duration_str)))
        return 0
    except:
        return 0
