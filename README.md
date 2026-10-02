# Corporate Carbon Footprint Analytics & Forecasting Pipeline

An end-to-end data analytics and forecasting project analyzing corporate carbon emissions across 50 companies and 5 industry sectors using Python, MySQL, and Power BI.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-ML-green)

---

## Project Overview

| Item | Detail |
|---|---|
| Dataset | 18,250 daily records |
| Companies | 50 companies |
| Sectors | 5 (Manufacturing, Agriculture, Energy, Transport, IT) |
| Industries | 4 (Automotive, Steel, Cement, Logistics) |
| Date Range | 2024 (daily) |
| Forecast Range | 2027 – 2033 |

---

## Key Results

| Metric | Value |
|---|---|
| Total Emissions (2024) | 590,663 tCO2e |
| Avg Daily Emission | 32.37 tCO2e |
| Peak Emission | 86.57 tCO2e |
| Renewable Energy Share | 35.11% |
| Total Carbon Tax | $20,614,128 |
| ML Model | Linear Regression |
| R² Score | 0.9878 |
| MAE | 57.73 tCO2e |
| 2033 Forecast | 725,392 tCO2e/year |
| Projected Growth | +22.81% by 2033 |

---

## Project Structure

```
corporate-carbon-footprint-pipeline/
├── phase1_data_cleaning.py       # Data cleaning & feature engineering
├── phase2_mysql_setup.sql        # MySQL table creation & 15 analytics queries
├── phase2_load_data.py           # Load cleaned CSV into MySQL
├── phase3_ml_forecasting.py      # Linear Regression forecast 2027-2033
├── climate_forecast.csv          # ML forecast output (120 rows)
├── forecast_chart.png            # Forecast visualization
├── requirements.txt              # Python dependencies
└── README.md
```

---

## How to Run

**Step 1 — Install dependencies**
```
pip install -r requirements.txt
```

**Step 2 — Clean the data**
```
python phase1_data_cleaning.py
```

**Step 3 — Set up MySQL**
- Open MySQL Workbench
- Run `phase2_mysql_setup.sql`

**Step 4 — Load data into MySQL**
- Edit DB credentials in `phase2_load_data.py`
```
python phase2_load_data.py
```

**Step 5 — Run ML forecast**
```
python phase3_ml_forecasting.py
```

**Step 6 — Open Power BI Dashboard**
- Load `cleaned_carbon_emissions.csv` as `EmissionsData`
- Load `climate_forecast.csv` as `ForecastData`
- Build 3-page dashboard per `phase5_powerbi_dashboard_design.md`

---

## Dashboard Pages

| Page | Name | Visuals |
|---|---|---|
| 1 | Executive Overview | 6 KPI cards, Line trend, Donut, Bar, Treemap |
| 2 | Facility Analysis | Top-10 bar, Transport chart, Strategy comparison, Matrix heatmap, Scatter plot |
| 3 | Forecast & Scenario | Forecast timeline, Annual forecast, Green Tax What-If slider |

---

## Forecast Summary (2027–2033)

| Year | Annual Emissions (tCO2e) |
|---|---|
| 2027 | 635,541 |
| 2028 | 650,516 |
| 2029 | 665,491 |
| 2030 | 680,466 |
| 2031 | 695,442 |
| 2032 | 710,417 |
| 2033 | 725,392 |

---

## Author

**Pranjal Choubey**
GitHub: [Pran-jal25](https://github.com/Pran-jal25)
