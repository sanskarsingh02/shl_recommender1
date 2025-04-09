import pandas as pd
import re

def get_recommendations(skills):
    print("Skills received:", skills)
    try:
        df = pd.read_csv("data/shl_dataset.csv")
        df.columns = df.columns.str.strip()
        print("CSV Columns:", df.columns.tolist())
        print("\nFirst few rows:")
        print(df.head(3).to_string())
    except Exception as e:
        print("Error reading CSV:", e)
        return []

    # Ensure the 'Skills' column exists
    if "Skills" not in df.columns:
        print("❌ 'Skills' column not found in CSV!")
        return []

    # Compile search pattern
    pattern = re.compile("|".join(re.escape(skill.lower()) for skill in skills), re.IGNORECASE)

    # Search in the Skills column
    df["__match"] = df["Skills"].apply(lambda x: bool(pattern.search(str(x))))
    matched_df = df[df["__match"]]

    print("✅ Matches found:", len(matched_df))
    if not matched_df.empty:
        print(matched_df[["Assessment Name", "Skills"]].head().to_string())

    return matched_df.head(5).to_dict(orient="records")
