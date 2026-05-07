# Streamlit dashboard for the MAT 550 final time series project

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(
    page_title="Electricity Demand Forecast Dashboard",
    page_icon="📈",
    layout="wide"
)


# -----------------------------
# Load data
# -----------------------------

@st.cache_data
def load_data():
    historical = pd.read_csv("data/historical_electricity_demand.csv")
    future_forecasts = pd.read_csv("data/future_forecasts_60_months.csv")
    model_comparison = pd.read_csv("data/final_model_comparison_all_models.csv")
    selected_models = pd.read_csv("data/final_selected_models_by_series.csv")
    residual_diagnostics = pd.read_csv("data/selected_model_residual_diagnostics.csv")
    residual_values = pd.read_csv("data/selected_model_residuals_for_dashboard.csv")

    historical["date"] = pd.to_datetime(historical["date"])
    future_forecasts["date"] = pd.to_datetime(future_forecasts["date"])
    residual_values["date"] = pd.to_datetime(residual_values["date"])

    return (
        historical,
        future_forecasts,
        model_comparison,
        selected_models,
        residual_diagnostics,
        residual_values
    )


(
    historical,
    future_forecasts,
    model_comparison,
    selected_models,
    residual_diagnostics,
    residual_values
) = load_data()


# -----------------------------
# Dashboard title
# -----------------------------

st.title("Electricity Demand Forecast Dashboard")

st.markdown(
    """
    This dashboard explores monthly electricity demand across major sectors and provides
    selected model forecasts for future planning. The goal is to help a non-technical
    decision maker compare sector trends, inspect forecast uncertainty, and understand
    how the selected models perform.
    """
)


# -----------------------------
# Sidebar controls
# -----------------------------

series_options = sorted(historical["series"].unique())

selected_series = st.sidebar.selectbox(
    "Select target series",
    series_options
)

forecast_horizon = st.sidebar.slider(
    "Forecast horizon to display",
    min_value=12,
    max_value=60,
    value=24,
    step=12
)


# -----------------------------
# Filter data
# -----------------------------

historical_series = historical[
    historical["series"] == selected_series
].copy()

forecast_series = future_forecasts[
    (future_forecasts["series"] == selected_series) &
    (future_forecasts["forecast_horizon_month"] <= forecast_horizon)
].copy()

selected_model_row = selected_models[
    selected_models["series"] == selected_series
].copy()

diagnostic_row = residual_diagnostics[
    residual_diagnostics["series"] == selected_series
].copy()

residual_series = residual_values[
    residual_values["series"] == selected_series
].copy()

comparison_series = model_comparison[
    model_comparison["series"] == selected_series
].copy()


# -----------------------------
# Selected model summary
# -----------------------------

st.subheader(f"Selected Forecast Model: {selected_series.title()}")

if not selected_model_row.empty:
    model_family = selected_model_row["model_family"].iloc[0]
    model_name = selected_model_row["model"].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Model family", model_family)

    with col2:
        st.metric("Selected model", model_name)
else:
    st.warning("No selected model information is available for this series.")


# -----------------------------
# Historical data and forecast plot
# -----------------------------

st.subheader("Historical Data with 60 Month Forecast")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=historical_series["date"],
        y=historical_series["actual"],
        mode="lines",
        name="Historical actual"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast_series["date"],
        y=forecast_series["forecast"],
        mode="lines",
        name="Forecast"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast_series["date"],
        y=forecast_series["upper_95"],
        mode="lines",
        name="Upper 95% interval",
        line=dict(width=0),
        showlegend=False
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast_series["date"],
        y=forecast_series["lower_95"],
        mode="lines",
        name="Lower 95% interval",
        fill="tonexty",
        line=dict(width=0),
        showlegend=True
    )
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Electricity demand",
    hovermode="x unified",
    legend_title="Series"
)

st.plotly_chart(fig, use_container_width=True)

if not forecast_series.empty:
    interval_method = forecast_series["interval_method"].iloc[0]
    st.caption(f"Prediction interval method: {interval_method}")


# -----------------------------
# Forecast table
# -----------------------------

st.subheader("Forecast Values")

forecast_display = forecast_series[
    [
        "date",
        "series",
        "model_family",
        "model",
        "forecast",
        "lower_95",
        "upper_95",
        "forecast_horizon_month"
    ]
].copy()

st.dataframe(
    forecast_display,
    use_container_width=True
)


# -----------------------------
# Residual diagnostics
# -----------------------------

st.subheader("Residual Diagnostics")

if not diagnostic_row.empty:
    diag = diagnostic_row.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Mean residual", round(diag["residual_mean"], 3))

    with col2:
        st.metric("Residual std.", round(diag["residual_std"], 3))

    with col3:
        st.metric("Ljung-Box p-value, lag 12", round(diag["ljung_box_pvalue_lag_12"], 4))

    with col4:
        st.metric("Ljung-Box p-value, lag 24", round(diag["ljung_box_pvalue_lag_24"], 4))

    st.caption(diag["diagnostic_note"])
else:
    st.warning("No residual diagnostic information is available for this series.")


fig_resid = go.Figure()

fig_resid.add_trace(
    go.Scatter(
        x=residual_series["date"],
        y=residual_series["error"],
        mode="lines+markers",
        name="Residual"
    )
)

fig_resid.add_hline(
    y=0,
    line_dash="dash"
)

fig_resid.update_layout(
    xaxis_title="Date",
    yaxis_title="Residual, actual minus forecast",
    hovermode="x unified"
)

st.plotly_chart(fig_resid, use_container_width=True)


# -----------------------------
# Model comparison table
# -----------------------------

st.subheader("Model Accuracy Comparison")

if not comparison_series.empty:
    display_cols = [
        col for col in [
            "series",
            "model_family",
            "model",
            "MAE",
            "RMSE",
            "MAPE",
            "sMAPE"
        ]
        if col in comparison_series.columns
    ]

    comparison_display = comparison_series[display_cols].copy()

    st.dataframe(
        comparison_display.sort_values("RMSE"),
        use_container_width=True
    )
else:
    st.warning("No model comparison data is available for this series.")


# -----------------------------
# Interpretation
# -----------------------------

st.subheader("How to Read This Dashboard")

st.markdown(
    """
    The historical line shows observed electricity demand. The forecast line extends
    the selected model into the future for the number of months chosen in the sidebar.
    The shaded band shows the 95% prediction interval, which gives a practical sense
    of forecast uncertainty.

    The residual diagnostics section checks how well the selected model handled the
    test period. Residuals close to zero indicate better forecasts. The Ljung-Box
    p-values help identify whether meaningful autocorrelation remains in the forecast
    errors. Larger p-values are generally better because they suggest less remaining
    pattern in the residuals.
    """
)
