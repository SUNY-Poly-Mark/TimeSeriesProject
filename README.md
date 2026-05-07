# TimeSeriesProject
# Electricity Demand Forecast Dashboard

This repository contains the reproducible notebook and Streamlit dashboard for my MAT 550 Time Series Analysis final project.

## Project Overview

This project analyzes monthly U.S. electricity demand across major sectors, including residential, commercial, industrial, transportation, and total electricity sales. The goal is to compare time series forecasting methods and communicate future demand patterns in a way that is useful for planning and decision making.

The analysis treats each sector as an individual time series and also considers the sectors as related components of the broader electricity demand system.

## Models Compared

The project compares several families of models covered in the course:

- Baseline forecasting models
- Exponential smoothing models, including Holt and Holt-Winters methods
- Box-Jenkins models, including ARIMA and SARIMA models
- Machine learning models, including tree-based models and a neural network

The final dashboard displays the selected model for each target series, future forecasts, prediction intervals, residual diagnostics, and accuracy comparisons across models.

## Streamlit Dashboard

The deployed dashboard is available here:

https://timeseriesproject-darcy.streamlit.app/

The dashboard allows a user to:

- Select a target electricity demand series
- Choose a forecast horizon up to 60 months
- View historical data with overlaid forecasts
- Inspect 95% prediction intervals
- Review residual diagnostics
- Compare model accuracy across implemented models

## Repository Structure

```text
TimeSeriesProject/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── historical_electricity_demand.csv
│   ├── future_forecasts_60_months.csv
│   ├── final_model_comparison_all_models.csv
│   ├── final_selected_models_by_series.csv
│   ├── selected_model_forecast_errors.csv
│   ├── selected_forecasts_for_dashboard.csv
│   ├── selected_model_residual_diagnostics.csv
│   └── selected_model_residuals_for_dashboard.csv
└── notebook/
    └── MAT550_FinalProject_DArcy.ipynb
