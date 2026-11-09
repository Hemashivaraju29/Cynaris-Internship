
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from forecasting_utils import (
    load_sales_data,
    filter_sales_data,
    aggregate_monthly_sales,
    forecast_sales,
    evaluate_forecast,
)


st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Forecasting Dashboard")
st.caption(
    "Explore historical sales, analyse business performance, "
    "and forecast the next three months."
)


@st.cache_data
def get_sales_data():
    return load_sales_data()


try:
    sales_df = get_sales_data()

    # Sidebar filters
    st.sidebar.header("Dashboard Filters")

    regions = ["All"] + sorted(sales_df["Region"].unique().tolist())
    categories = ["All"] + sorted(
        sales_df["Category"].unique().tolist()
    )

    selected_region = st.sidebar.selectbox(
        "Select Region", regions
    )
    selected_category = st.sidebar.selectbox(
        "Select Category", categories
    )

    filtered_df = filter_sales_data(
        sales_df,
        region=selected_region,
        category=selected_category
    )

    if filtered_df.empty:
        st.warning("No sales records found for the selected filters.")
        st.stop()

    # Data preparation
    monthly_df = aggregate_monthly_sales(filtered_df)
    forecast_df = forecast_sales(monthly_df, periods=3, window=3)
    evaluation = evaluate_forecast(
        monthly_df, window=3, test_size=3
    )

    # KPI metrics
    st.subheader("Business Performance")

    total_sales = filtered_df["Sales"].sum()
    average_monthly_sales = monthly_df["Sales"].mean()
    total_units = filtered_df["Units Sold"].sum()
    next_month_forecast = forecast_df.iloc[0]["Forecast Sales"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"₹{total_sales:,.0f}")
    col2.metric(
        "Average Monthly Sales",
        f"₹{average_monthly_sales:,.0f}"
    )
    col3.metric("Units Sold", f"{total_units:,.0f}")
    col4.metric(
        "Next Month Forecast",
        f"₹{next_month_forecast:,.0f}"
    )

    st.divider()

    # Historical sales chart
    st.subheader("Monthly Sales Trend")

    historical_fig = px.line(
        monthly_df,
        x="Month",
        y="Sales",
        markers=True,
        title="Historical Monthly Sales",
        labels={
            "Month": "Month",
            "Sales": "Sales (₹)"
        }
    )

    historical_fig.update_layout(
        hovermode="x unified",
        xaxis_title="Month",
        yaxis_title="Sales (₹)"
    )

    st.plotly_chart(historical_fig, use_container_width=True)

    # Forecast chart
    st.subheader("Future Sales Forecast")

    forecast_fig = go.Figure()

    forecast_fig.add_trace(
        go.Scatter(
            x=monthly_df["Month"],
            y=monthly_df["Sales"],
            mode="lines+markers",
            name="Historical Sales"
        )
    )

    forecast_fig.add_trace(
        go.Scatter(
            x=forecast_df["Month"],
            y=forecast_df["Forecast Sales"],
            mode="lines+markers",
            name="Forecast Sales",
            line=dict(dash="dash")
        )
    )

    forecast_fig.update_layout(
        title="Historical Sales vs Next 3 Months Forecast",
        xaxis_title="Month",
        yaxis_title="Sales (₹)",
        hovermode="x unified"
    )

    st.plotly_chart(forecast_fig, use_container_width=True)

    # Model evaluation
    st.subheader("Forecast Model Evaluation")

    metric1, metric2 = st.columns(2)

    metric1.metric("Mean Absolute Error (MAE)", f"₹{evaluation['MAE']:,.2f}")
    metric2.metric("Root Mean Squared Error (RMSE)", f"₹{evaluation['RMSE']:,.2f}")

    st.caption(
        "Evaluation uses a three-month historical holdout period. "
        "Lower MAE and RMSE values indicate smaller prediction errors."
    )

    # Forecast table and download
    st.subheader("Forecast Details")

    display_forecast = forecast_df.copy()
    display_forecast["Month"] = (
        display_forecast["Month"].dt.strftime("%B %Y")
    )
    display_forecast["Forecast Sales"] = (
        display_forecast["Forecast Sales"].round(2)
    )

    st.dataframe(display_forecast, use_container_width=True)

    csv_data = forecast_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Forecast CSV",
        data=csv_data,
        file_name="sales_forecast.csv",
        mime="text/csv"
    )

    # Region and category analysis
    st.divider()
    st.subheader("Sales Analysis")

    chart1, chart2 = st.columns(2)

    with chart1:
        region_sales = (
            filtered_df.groupby("Region", as_index=False)["Sales"]
            .sum()
        )

        region_fig = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            title="Sales by Region",
            labels={"Sales": "Sales (₹)"}
        )

        st.plotly_chart(region_fig, use_container_width=True)

    with chart2:
        category_sales = (
            filtered_df.groupby("Category", as_index=False)["Sales"]
            .sum()
        )

        category_fig = px.bar(
            category_sales,
            x="Category",
            y="Sales",
            title="Sales by Category",
            labels={"Sales": "Sales (₹)"}
        )

        st.plotly_chart(category_fig, use_container_width=True)

    # Raw data
    with st.expander("View Filtered Sales Data"):
        st.dataframe(filtered_df, use_container_width=True)

    st.caption(
        "Note: Forecasts use a three-month moving average. "
        "The dataset is small, so predictions are illustrative "
        "and should not be treated as guaranteed sales."
    )

except FileNotFoundError as error:
    st.error(f"Dataset file not found: {error}")

except Exception as error:
    st.error(f"Dashboard error: {error}")
