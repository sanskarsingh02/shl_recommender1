# run.py
from app.api import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets this PORT env var
    app.run(debug=True, host="0.0.0.0", port=port)
