
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.title("HHS Care Demand Forecast Dashboard")

st.sidebar.header("Forecast Settings")

# LOAD DATA
forecast_df = pd.read_csv(r"C:\Users\91701\OneDrive\Desktop\hhs-care-demand-forecast\data\forecast_predictions.csv")
kpi_table = pd.read_csv(r"C:\Users\91701\OneDrive\Desktop\hhs-care-demand-forecast\data\kpi_table.csv")

# MODEL SELECTION
model = st.sidebar.selectbox(
    "Select Model",
    ["RF", "ETS", "ARIMA"]
)

# HORIZON SELECTION
horizon = st.sidebar.selectbox(
    "Forecast Horizon",
    ["1D", "7D", "14D"]
)

# SELECT COLUMNS BASED ON USER CHOICE
actual_col = f"Actual_{horizon}"
pred_col = f"{model}_{horizon}"

actual = forecast_df[actual_col]
predictions = forecast_df[pred_col]

st.write("Selected Model:", model)
st.write("Forecast Horizon:", horizon)

# FUTURE CARE LOAD FORECAST CHART
st.subheader("Future Care Load Forecast")

fig = go.Figure()

fig.add_trace(go.Scatter(
    y=actual,
    mode='lines',
    name='Actual',
    line=dict(color='red')
))

fig.add_trace(go.Scatter(
    y=predictions,
    mode='lines',
    name='Forecast',
    line=dict(color='blue', dash='dash')
))

fig.update_layout(
    title="Future Care Load Forecast",
    xaxis_title="Time",
    yaxis_title="Care Demand",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# DISCHARGE DEMAND FORECAST PANEL
st.subheader("Discharge Demand Forecast")

st.metric(
    "Predicted Discharge Demand (Latest)",
    round(predictions.iloc[-1], 2)
)

# MODEL SELECTION & COMPRISON

st.subheader("Model Performance")
st.dataframe(kpi_table)

# CONFIDENCE INTERVAL (usually used for ARIMA forecast)
if model == "ARIMA":

    lower_conf = predictions * 0.95
    upper_conf = predictions * 1.05

    fig2 = go.Figure()

    # Forecast line
    fig2.add_trace(go.Scatter(
        y=predictions,
        mode="lines",
        name="Forecast",
        line=dict(color="blue")
    ))

    # Upper confidence
    fig2.add_trace(go.Scatter(
        y=upper_conf,
        mode="lines",
        line=dict(width=0),
        showlegend=False
    ))

    # Lower confidence (creates shaded area)
    fig2.add_trace(go.Scatter(
        y=lower_conf,
        mode="lines",
        fill='tonexty',
        fillcolor='rgba(0,100,255,0.2)',
        line=dict(width=0),
        name="Confidence Interval"
    ))

    fig2.update_layout(
        title="ARIMA Confidence Interval",
        xaxis_title="Time",
        yaxis_title="Care Demand",
        hovermode="x unified"
    )

    st.subheader("Confidence Interval Visualization")
    st.plotly_chart(fig2, use_container_width=True)

# SCENARIO COMPARISON VIEW
st.sidebar.subheader("Scenario Comparison")

models_compare = st.sidebar.multiselect(
    "Compare Models",
    ["RF", "ETS", "ARIMA"]
)

if models_compare:

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        y=actual,
        mode='lines',
        name='Actual',
        line=dict(color='yellow')
    ))

    for m in models_compare:
        col = f"{m}_{horizon}"

        fig3.add_trace(go.Scatter(
            y=forecast_df[col],
            mode='lines',
            name=m
        ))

    fig3.update_layout(
        title="Model Comparison",
        xaxis_title="Time",
        yaxis_title="Care Demand",
        hovermode="x unified"
    )


    st.plotly_chart(fig3, use_container_width=True)
