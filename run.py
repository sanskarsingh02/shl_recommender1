# shl_recommender/run.py
from app.api import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use 10000 or Render-assigned port
    app.run(debug=True, host="0.0.0.0", port=port)
