import pandas as pd
import json

with open("grievance_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.json_normalize(data)

df.to_csv("clean_data.csv", index=False)