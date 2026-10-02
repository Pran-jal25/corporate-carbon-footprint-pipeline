CREATE DATABASE IF NOT EXISTS carbon_analytics;
USE carbon_analytics;
DROP TABLE IF EXISTS carbon_emissions;

CREATE TABLE carbon_emissions (
    id                                  INT AUTO_INCREMENT PRIMARY KEY,
    Company_ID                          VARCHAR(10),
    Date                                DATE,
    Year                                SMALLINT,
    Month                               TINYINT,
    Quarter                             TINYINT,
    Month_Name                          VARCHAR(3),
    Sector                              VARCHAR(50),
    Industry_Sectors                    VARCHAR(100),
    Carbon_Reduction_Strategy           VARCHAR(100),
    Supply_Chain_Transport_Mode         VARCHAR(20),
    Total_Energy_Consumption_kWh        DECIMAL(12,2),
    Renewable_Energy_Consumption_kWh    DECIMAL(12,2),
    NonRenewable_Energy_Consumption_kWh DECIMAL(12,2),
    Renewable_Share_Pct                 DECIMAL(6,2),
    Production_Output_Units             DECIMAL(12,2),
    Supply_Chain_Transport_km           DECIMAL(10,2),
    Raw_Material_Usage_kg               DECIMAL(12,2),
    Employment_Count                    INT,
    Process_Efficiency_Percent          DECIMAL(5,2),
    Carbon_Emission_tCO2e_TARGET        DECIMAL(10,4),
    Carbon_Intensity                    DECIMAL(10,6),
    Energy_Cost_USD                     DECIMAL(12,2),
    Carbon_Tax_USD                      DECIMAL(12,2),
    Energy_Cost_per_kWh                 DECIMAL(8,4),
    Strategy_Implementation_Cost_USD    DECIMAL(14,2),
    Expected_Carbon_Reduction_Percent   DECIMAL(5,2),
    Expected_Renewable_Share_Percent    DECIMAL(5,2),
    Public_Acceptance_Index             DECIMAL(4,2),
    Social_Impact_Score                 DECIMAL(4,2)
);

-- Data Quality Checks
SELECT COUNT(*) AS total_rows FROM carbon_emissions;
SELECT SUM(Company_ID IS NULL) AS null_company, SUM(Date IS NULL) AS null_date,
       SUM(Carbon_Emission_tCO2e_TARGET IS NULL) AS null_emissions FROM carbon_emissions;
SELECT COUNT(*) AS negatives FROM carbon_emissions WHERE Carbon_Emission_tCO2e_TARGET < 0;
SELECT Company_ID, Date, COUNT(*) FROM carbon_emissions GROUP BY Company_ID, Date HAVING COUNT(*) > 1;

-- Analytics Queries
-- Q1: Emissions by sector
SELECT Sector, ROUND(SUM(Carbon_Emission_tCO2e_TARGET),2) AS total, ROUND(AVG(Carbon_Emission_tCO2e_TARGET),2) AS avg
FROM carbon_emissions GROUP BY Sector ORDER BY total DESC;

-- Q2: Emissions by industry
SELECT Industry_Sectors, ROUND(SUM(Carbon_Emission_tCO2e_TARGET),2) AS total, COUNT(DISTINCT Company_ID) AS companies
FROM carbon_emissions GROUP BY Industry_Sectors ORDER BY total DESC;

-- Q3: Monthly emissions trend
SELECT Month, Month_Name, ROUND(SUM(Carbon_Emission_tCO2e_TARGET),2) AS monthly_total
FROM carbon_emissions GROUP BY Month, Month_Name ORDER BY Month;

-- Q4: Quarterly summary
SELECT Quarter, ROUND(SUM(Carbon_Emission_tCO2e_TARGET),2) AS total,
       ROUND(SUM(Carbon_Tax_USD),2) AS tax FROM carbon_emissions GROUP BY Quarter ORDER BY Quarter;

-- Q5: Top 10 companies
SELECT Company_ID, Sector, ROUND(SUM(Carbon_Emission_tCO2e_TARGET),2) AS total
FROM carbon_emissions GROUP BY Company_ID, Sector ORDER BY total DESC LIMIT 10;

-- Q6: Renewable share by sector
SELECT Sector, ROUND(AVG(Renewable_Share_Pct),2) AS avg_renewable_pct
FROM carbon_emissions GROUP BY Sector ORDER BY avg_renewable_pct DESC;

-- Q7: Strategy effectiveness
SELECT Carbon_Reduction_Strategy, ROUND(AVG(Expected_Carbon_Reduction_Percent),2) AS expected_reduction,
       ROUND(AVG(Strategy_Implementation_Cost_USD),2) AS avg_cost
FROM carbon_emissions GROUP BY Carbon_Reduction_Strategy ORDER BY expected_reduction DESC;

-- Q8: Transport mode vs emissions
SELECT Supply_Chain_Transport_Mode, ROUND(AVG(Carbon_Emission_tCO2e_TARGET),2) AS avg_emission
FROM carbon_emissions GROUP BY Supply_Chain_Transport_Mode ORDER BY avg_emission DESC;

-- Q9: Carbon tax by sector
SELECT Sector, ROUND(SUM(Carbon_Tax_USD),2) AS total_tax
FROM carbon_emissions GROUP BY Sector ORDER BY total_tax DESC;

-- Q10: Energy cost per kWh by industry
SELECT Industry_Sectors, ROUND(AVG(Energy_Cost_per_kWh),4) AS avg_cost_per_kWh
FROM carbon_emissions GROUP BY Industry_Sectors ORDER BY avg_cost_per_kWh DESC;

-- Q11: Carbon intensity by sector
SELECT Sector, ROUND(AVG(Carbon_Intensity),6) AS avg_intensity
FROM carbon_emissions GROUP BY Sector ORDER BY avg_intensity DESC;

-- Q12: Companies above average emissions
SELECT Company_ID, Sector, ROUND(AVG(Carbon_Emission_tCO2e_TARGET),2) AS avg_emission
FROM carbon_emissions GROUP BY Company_ID, Sector
HAVING AVG(Carbon_Emission_tCO2e_TARGET) > (SELECT AVG(Carbon_Emission_tCO2e_TARGET) FROM carbon_emissions)
ORDER BY avg_emission DESC;

-- Q13: Monthly energy vs emissions
SELECT Month, Month_Name, ROUND(SUM(Total_Energy_Consumption_kWh),2) AS energy,
       ROUND(SUM(Carbon_Emission_tCO2e_TARGET),2) AS emissions
FROM carbon_emissions GROUP BY Month, Month_Name ORDER BY Month;

-- Q14: Social score vs emissions
SELECT Sector, ROUND(AVG(Social_Impact_Score),2) AS social_score,
       ROUND(AVG(Carbon_Emission_tCO2e_TARGET),2) AS avg_emission
FROM carbon_emissions GROUP BY Sector ORDER BY avg_emission DESC;

-- Q15: Strategy cost vs expected reduction
SELECT Carbon_Reduction_Strategy, ROUND(AVG(Strategy_Implementation_Cost_USD),2) AS avg_cost,
       ROUND(AVG(Expected_Carbon_Reduction_Percent),2) AS expected_reduction
FROM carbon_emissions GROUP BY Carbon_Reduction_Strategy ORDER BY avg_cost DESC;
