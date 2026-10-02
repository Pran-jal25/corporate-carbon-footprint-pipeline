import pandas as pd, numpy as np, matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings; warnings.filterwarnings("ignore")

df = pd.read_csv("cleaned_carbon_emissions.csv", parse_dates=["Date"])

# Monthly actuals 2024
monthly = df.groupby(["Year","Month"]).agg(Total_Emissions=("Carbon_Emission_tCO2e_TARGET","sum")).reset_index()
monthly["Data_Type"] = "Historical"

# Simulate 2025-2026 (+2.5%/yr)
m, s = monthly["Total_Emissions"].mean(), monthly["Total_Emissions"].std()
sim = pd.DataFrame([{"Year":y,"Month":mo,"Total_Emissions":round(m*(1.025**(y-2024))+np.random.normal(0,s*0.05),4),"Data_Type":"Simulated"}
for y in [2025,2026] for mo in range(1,13)])

train = pd.concat([monthly[["Year","Month","Total_Emissions","Data_Type"]], sim], ignore_index=True)
train["Month_Index"] = (train["Year"]-2024)*12 + train["Month"]

X, y = train[["Year","Month","Month_Index"]], train["Total_Emissions"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression().fit(X_tr, y_tr)
print(f"MAE: {mean_absolute_error(y_te, model.predict(X_te)):.2f}  R²: {r2_score(y_te, model.predict(X_te)):.4f}")

# Forecast 2027-2033
fc = pd.DataFrame([{"Year":y,"Month":mo,"Month_Index":(y-2024)*12+mo,
                    "Total_Emissions":round(model.predict(pd.DataFrame([[y,mo,(y-2024)*12+mo]],columns=["Year","Month","Month_Index"]))[0],4),
                    "Data_Type":"Forecast"} for y in range(2027,2034) for mo in range(1,13)])

final = pd.concat([monthly[["Year","Month","Total_Emissions","Data_Type"]].assign(Month_Index=lambda d:(d.Year-2024)*12+d.Month),
                   sim.assign(Month_Index=lambda d:(d.Year-2024)*12+d.Month), fc], ignore_index=True)
final["Date"] = pd.to_datetime(final["Year"].astype(str)+"-"+final["Month"].astype(str).str.zfill(2)+"-01")
final = final[["Date","Year","Month","Month_Index","Total_Emissions","Data_Type"]].sort_values(["Year","Month"])
final.to_csv("climate_forecast.csv", index=False)
print("Saved: climate_forecast.csv")

# Plot
fig, ax = plt.subplots(figsize=(14,6))
for dtype, color, style, marker in [("Historical","#2196F3","-","o"),("Simulated","#FF9800","--","s"),("Forecast","#F44336",":","^")]:
    d = final[final["Data_Type"]==dtype]
    ax.plot(d["Date"], d["Total_Emissions"], color=color, linestyle=style, marker=marker, linewidth=2, label=dtype)
ax.axvline(pd.Timestamp("2027-01-01"), color="gray", linestyle="--", alpha=0.5)
ax.set(title="Monthly Carbon Emissions: Historical vs Forecast (2024-2033)", xlabel="Date", ylabel="tCO2e")
ax.legend(); ax.grid(alpha=0.3); plt.tight_layout()
plt.savefig("forecast_chart.png", dpi=150); print("Saved: forecast_chart.png")
plt.show()
