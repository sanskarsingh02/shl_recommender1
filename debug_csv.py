import pandas as pd

df = pd.read_csv("data/shl_dataset.csv")
print("CSV Columns:", df.columns.tolist())
print("\nFirst 3 Rows:")
print(df.head(3).to_string())
