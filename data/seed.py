import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://dev:dev@localhost:5432/healthcare"
engine = create_engine(DATABASE_URL)

df = pd.read_csv("data/timely_care.csv")

# standardize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

df = df[[
    "facility_id",
    "facility_name",
    "state",
    "measure_id",
    "measure_name",
    "score",
    "start_date",
    "end_date"
]]

# drop rows with no score
df = df[df["score"].notna()]
df = df[df["score"] != "Not Available"]
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df = df.dropna(subset=["score"])

# parse dates
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

df = df.reset_index(drop=True)
df.index = df.index + 1
df.to_sql("hospital_metrics", engine, if_exists="replace", index=True, index_label="id")
print(f"Seeded {len(df)} rows from {df['facility_name'].nunique()} hospitals across {df['state'].nunique()} states.")
