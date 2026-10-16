
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dash_table, dcc, html

# Load and prepare the sales dataset
DATA_FILE = Path(__file__).with_name("Sales_Data.csv")

df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
df["Month"] = df["Date"].dt.strftime("%Y-%m")

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Sales Performance Dashboard"),
        html.P("Explore sales performance by region, category, and date."),

        html.Div(
            [
                html.Div(
                    [
                        html.Label("Region"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in sorted(df["Region"].unique())
                            ],
                            multi=True,
                            placeholder="All regions",
                        ),
                    ],
                    style={"width": "30%"},
                ),
                html.Div(
                    [
                        html.Label("Category"),
                        dcc.Dropdown(
                            id="category-filter",
                            options=[
                                {"label": category, "value": category}
                                for category in sorted(df["Category"].unique())
                            ],
                            multi=True,
                            placeholder="All categories",
                        ),
                    ],
                    style={"width": "30%"},
                ),
                html.Div(
                    [
                        html.Label("Date range"),
                        dcc.DatePickerRange(
                            id="date-filter",
                            min_date_allowed=df["Date"].min().date(),
                            max_date_allowed=df["Date"].max().date(),
                            start_date=df["Date"].min().date(),
                            end_date=df["Date"].max().date(),
                        ),
                    ],
                    style={"width": "40%"},
                ),
            ],
            style={"display": "flex", "gap": "15px", "marginBottom": "25px"},
        ),

        dcc.Graph(id="monthly-sales-chart"),
        dcc.Graph(id="monthly-units-chart"),
        dcc.Graph(id="category-sales-chart"),

        html.H2("Filtered Sales Records"),
        dash_table.DataTable(
            id="sales-table",
            columns=[
                {"name": column, "id": column}
                for column in [
                    "Date", "Region", "Category", "Sales", "Units Sold", "Month"
                ]
            ],
            page_size=8,
            sort_action="native",
            filter_action="native",
            style_table={"overflowX": "auto"},
            style_cell={"padding": "10px", "textAlign": "left"},
            style_header={"fontWeight": "bold"},
        ),
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "maxWidth": "1200px",
        "margin": "auto",
        "padding": "24px",
    },
)


@app.callback(
    Output("monthly-sales-chart", "figure"),
    Output("monthly-units-chart", "figure"),
    Output("category-sales-chart", "figure"),
    Output("sales-table", "data"),
    Input("region-filter", "value"),
    Input("category-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def update_dashboard(regions, categories, start_date, end_date):
    filtered = df.copy()

    if regions:
        filtered = filtered[filtered["Region"].isin(regions)]

    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]

    if start_date:
        filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]

    if end_date:
        filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]

    monthly = (
        filtered.groupby("Month", as_index=False)
        .agg(Sales=("Sales", "sum"), Units_Sold=("Units Sold", "sum"))
        .sort_values("Month")
    )

    sales_fig = px.line(
        monthly,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales",
    )
    sales_fig.update_layout(xaxis_title="Month", yaxis_title="Sales")

    units_fig = px.bar(
        monthly,
        x="Month",
        y="Units_Sold",
        title="Monthly Units Sold",
    )
    units_fig.update_layout(xaxis_title="Month", yaxis_title="Units Sold")

    category_totals = (
        filtered.groupby("Category", as_index=False)["Sales"]
        .sum()
    )
    category_fig = px.pie(
        category_totals,
        names="Category",
        values="Sales",
        title="Category Sales Distribution",
    )

    table_data = filtered.copy()
    table_data["Date"] = table_data["Date"].dt.strftime("%Y-%m-%d")

    return (
        sales_fig,
        units_fig,
        category_fig,
        table_data[
            ["Date", "Region", "Category", "Sales", "Units Sold", "Month"]
        ].to_dict("records"),
    )


if __name__ == "__main__":
    app.run(debug=True)
