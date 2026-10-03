import pandas as pd

df = pd.read_csv("agriculture_raw_dummy.csv")
df["crop"] = df["crop"].astype(str).str.strip().str.title()
df["district"] = df["district"].astype(str).str.strip().str.title()
df["date"] = pd.to_datetime(df["date"], errors="coerce")

for col in ["production_tonnes", "price_per_kg", "stock_units"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.drop_duplicates()
df.loc[df["production_tonnes"].isna(), "production_tonnes"] = df["production_tonnes"].median()

valid_price_median = df.loc[df["price_per_kg"] > 0, "price_per_kg"].median()
df.loc[df["price_per_kg"] <= 0, "price_per_kg"] = valid_price_median

df["total_value"] = df["production_tonnes"] * 1000 * df["price_per_kg"]
df.to_csv("agriculture_cleaned_week2.csv", index=False)
print(df.head())
