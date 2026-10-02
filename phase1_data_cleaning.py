import pandas as pd
import numpy as np

df = pd.read_csv("carbon_emission_dataset_with_Industry.csv")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce") #if date is wrong then it wrote "NAT" ie not a date in place of that;

num_cols = [c for c in df.columns if df[c].dtype in ["float64", "int64"]]
cat_cols = ["Sector", "Supply_Chain_Transport_Mode", "Carbon_Reduction_Strategy", "Industry_Sectors"]
text_cols = cat_cols + ["Company_ID"]

for c in num_cols: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(df[c].median())
for c in cat_cols: df[c] = df[c].fillna(df[c].mode()[0])
for c in text_cols: df[c] = df[c].astype(str).str.strip().str.title()

df.drop_duplicates(inplace=True)
for c in ["Total_Energy_Consumption_kWh","Carbon_Emission_tCO2e_TARGET","Energy_Cost_USD","Carbon_Tax_USD"]:
    df = df[df[c] >= 0] #removing records having "0" or "negative" value;

df["Year"]= df["Date"].dt.year
df["Month"]= df["Date"].dt.month
df["Quarter"]= df["Date"].dt.quarter
df["Month_Name"]= df["Date"].dt.strftime("%b")
df["Renewable_Share_Pct"] = (df["Renewable_Energy_Consumption_kWh"] / df["Total_Energy_Consumption_kWh"].replace(0, np.nan) * 100).round(2)
df["Carbon_Intensity"]    = (df["Carbon_Emission_tCO2e_TARGET"] / df["Production_Output_Units"].replace(0, np.nan)).round(6)
df["Energy_Cost_per_kWh"] = (df["Energy_Cost_USD"] / df["Total_Energy_Consumption_kWh"].replace(0, np.nan)).round(4)

df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
df.to_csv("cleaned_carbon_emissions.csv", index=False)
print(f"Done: {df.shape[0]} rows, {df.shape[1]} cols → cleaned_carbon_emissions.csv")
