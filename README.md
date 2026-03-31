# economics-of-slavery

# Slavery and Industrial Development in the United States

## Overview
This project investigates the relationship between slavery intensity and industrial development in the United States during the 19th century. Using econometric methods, the analysis examines whether states with higher reliance on slavery experienced lower levels of manufacturing capital per capita.

The project is part of a broader cliometrics-style analysis combining historical data, economic theory, and regression modeling.

---

## Research Question
What is the relationship between the pre-Civil War slave population in the US and economic 
developments across US states by 1900?

---

## Hypothesis
- **Null Hypothesis (H₀):** There is no relationship between slavery intensity and industrial development  
- **Alternative Hypothesis (H₁):** Higher slavery intensity is associated with lower industrial development  

---

## Data
The dataset includes state-level observations with the following key variables:

- `manufacture_k_per_capita` (dependent variable)  
- `slaves_per_capita` (main independent variable)  
- `farms_per_capita` (control variable)  

The dataset contains **35 observations** across U.S. states.

---

## Methodology
The project uses **Ordinary Least Squares (OLS)** regression to estimate the relationship:

manufacture_k_per_capita = β₀ + β₁(slaves_per_capita) + β₂(farms_per_capita) + ε

Robust (heteroskedasticity-consistent) standard errors are also applied to ensure reliability.

---

## Key Results
- Slavery intensity has a **negative and statistically significant** relationship with industrial development  
- Coefficient on `slaves_per_capita`: **-373.11 (p < 0.001)**  
- Agricultural intensity (`farms_per_capita`) is also negative and significant  
- Model explains approximately **55% of variation (R² = 0.55)**  

These results suggest that states more reliant on slavery were systematically less industrialized.

---

## Visualizations

### Slavery vs Industrial Development
- Scatter plot shows a strong negative relationship between slavery intensity and manufacturing capital  

### State-Level Trends (1790–1860)
- Southern states (e.g., South Carolina, Georgia) saw large increases in slavery intensity  
- Northern states (e.g., Delaware) experienced declines  

---

## Tools & Technologies
- Python (pandas, numpy, statsmodels, matplotlib)  
- R (for supplementary analysis) 
