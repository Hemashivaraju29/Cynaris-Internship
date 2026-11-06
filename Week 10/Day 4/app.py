
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard_utils import (
    load_historical_data,
    load_forecast,
    load_metrics,
)


st.set_page_config(
    page_title="Reliance Stock Forecast Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Reliance Stock Forecasting Dashboard")
st.markdown(
    "Explore historical stock prices, Prophet forecasts, "
    "prediction intervals, and model performance."
)

# Load data
@st.cache_data
def get_dashboard_data():
    historical = load_historical_data()
    forecast = load_forecast()
    metrics = load_metrics()
    return historical, forecast, metrics


try:
    historical, forecast, metrics = get_dashboard_data()

    st.sidebar.header("Dashboard Controls")

    forecast_days = st.sidebar.slider(
        "Forecast horizon (business days)",
        min_value=5,
        max_value=len(forecast),
        value=min(30, len(forecast)),
        step=1,
    )

    selected_forecast = forecast.head(forecast_days)

    st.sidebar.success("Data loaded successfully")

    # Key performance indicators
    st.subheader("Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", f"{metrics['MAE']:,.2f}")
    col2.metric("RMSE", f"{metrics['RMSE']:,.2f}")
    col3.metric("MAPE", f"{metrics['MAPE']:.2f}%")

    st.caption(
        "Metrics are based on the W10D2 Prophet model evaluation "
        "using the final 20% of historical data."
    )

    # Historical stock prices
    st.subheader("Historical Stock Prices")

    historical_fig = go.Figure()

    historical_fig.add_trace(
        go.Scatter(
            x=historical["Date"],
            y=historical["Close"],
            mode="lines",
            name="Historical Closing Price",
            line=dict(width=2),
        )
    )

    historical_fig.update_layout(
        title="Reliance Historical Closing Price",
        xaxis_title="Date",
        yaxis_title="Closing Price",
        template="plotly_white",
        hovermode="x unified",
        height=450,
    )

    historical_fig.update_xaxes(rangeslider_visible=True)

    st.plotly_chart(historical_fig, use_container_width=True)

    # Forecast chart
    st.subheader("Future Stock Price Forecast")

    forecast_fig = go.Figure()

    forecast_fig.add_trace(
        go.Scatter(
            x=selected_forecast["ds"],
            y=selected_forecast["yhat_upper"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    forecast_fig.add_trace(
        go.Scatter(
            x=selected_forecast["ds"],
            y=selected_forecast["yhat_lower"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(0, 150, 255, 0.15)",
            name="Prediction Interval",
            hoverinfo="skip",
        )
    )

    forecast_fig.add_trace(
        go.Scatter(
            x=selected_forecast["ds"],
            y=selected_forecast["yhat"],
            mode="lines+markers",
            name="Forecasted Price",
            line=dict(width=3),
        )
    )

    forecast_fig.update_layout(
        title=f"Reliance Forecast - Next {forecast_days} Business Days",
        xaxis_title="Forecast Date",
        yaxis_title="Predicted Closing Price",
        template="plotly_white",
        hovermode="x unified",
        height=450,
    )

    st.plotly_chart(forecast_fig, use_container_width=True)

    # Forecast data table
    st.subheader("Forecast Details")

    display_forecast = selected_forecast[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].rename(
        columns={
            "ds": "Date",
            "yhat": "Predicted Price",
            "yhat_lower": "Lower Bound",
            "yhat_upper": "Upper Bound",
        }
    )

    st.dataframe(
        display_forecast.round(2),
        use_container_width=True,
        hide_index=True,
    )

    # Download forecast data
    csv_data = display_forecast.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Forecast CSV",
        data=csv_data,
        file_name="reliance_forecast.csv",
        mime="text/csv",
    )

    st.success("Forecast dashboard loaded successfully!")

except FileNotFoundError as error:
    st.error(f"Required data file not found: {error}")

except Exception as error:
    st.error(f"Unable to load dashboard: {error}")
