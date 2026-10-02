import pandas as pd
import mysql.connector

DB = {"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "carbon_analytics"}
COLS = ["Company_ID","Date","Year","Month","Quarter","Month_Name","Sector","Industry_Sectors",
        "Carbon_Reduction_Strategy","Supply_Chain_Transport_Mode","Total_Energy_Consumption_kWh",
        "Renewable_Energy_Consumption_kWh","NonRenewable_Energy_Consumption_kWh","Renewable_Share_Pct",
        "Production_Output_Units","Supply_Chain_Transport_km","Raw_Material_Usage_kg","Employment_Count",
        "Process_Efficiency_Percent","Carbon_Emission_tCO2e_TARGET","Carbon_Intensity","Energy_Cost_USD",
        "Carbon_Tax_USD","Energy_Cost_per_kWh","Strategy_Implementation_Cost_USD",
        "Expected_Carbon_Reduction_Percent","Expected_Renewable_Share_Percent",
        "Public_Acceptance_Index","Social_Impact_Score"]

df   = pd.read_csv("cleaned_carbon_emissions.csv")[COLS].where(pd.notnull, None)
conn = mysql.connector.connect(**DB)
cur  = conn.cursor()
cur.execute("DELETE FROM carbon_emissions;"); conn.commit()

sql  = f"INSERT INTO carbon_emissions ({','.join(COLS)}) VALUES ({','.join(['%s']*len(COLS))})"
rows = [tuple(r) for r in df.itertuples(index=False, name=None)]
for i in range(0, len(rows), 500):
    cur.executemany(sql, rows[i:i+500]); conn.commit()

cur.execute("SELECT COUNT(*) FROM carbon_emissions;")
print(f"Loaded: {cur.fetchone()[0]} rows")
cur.close(); conn.close()
