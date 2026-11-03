
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Pristyn Care | Healthcare Analytics",
    page_icon="🏥",
    layout="wide",
)


# --------------------------------------------------
# THEME-AWARE CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        padding: 2rem 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: var(--text-color) !important;
        font-weight: 700;
    }

    /* KPI Cards */
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 18px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.35);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div,
    [data-testid="stMetricDelta"] {
        color: var(--text-color) !important;
    }

    [data-testid="stMetricValue"] {
        font-weight: 700;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.25);
    }

    /* General spacing */
    div[data-testid="stPlotlyChart"] {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"


# --------------------------------------------------
# DASHBOARD TITLE
# --------------------------------------------------

st.title("🏥 Pristyn Care Health Analytics Dashboard")

st.caption(
    "Dashboard v1 | Appointment, Patient Satisfaction "
    "and Data Quality"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    files = {
        "appointment": "appointment_no_show_summary.csv",
        "department": "no_show_by_department.csv",
        "specialty": "no_show_by_specialty.csv",
        "age": "no_show_by_patient_age_group.csv",
        "insurance": "no_show_by_insurance_type.csv",
        "booking_hour": "no_show_by_booking_hour.csv",
        "satisfaction": "satisfaction_rating_summary.csv",
        "hospital": "satisfaction_by_hospital.csv",
        "satisfaction_department": "satisfaction_by_department.csv",
        "resource_quality": "resource_data_quality_report.csv",
    }

    result = {}

    for key, filename in files.items():

        path = OUTPUT_DIR / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Missing required file: {path}"
            )

        result[key] = pd.read_csv(path)

    return result


try:
    data = load_data()

except Exception as error:

    st.error(
        f"Unable to load dashboard data: {error}"
    )

    st.info(
        "Run the project analysis scripts to generate "
        "the required CSV files."
    )

    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

st.sidebar.caption(
    "Explore appointment records"
)

department_source = data["department"]
specialty_source = data["specialty"]
insurance_source = data["insurance"]


selected_department = st.sidebar.multiselect(
    "Select Department",
    options=sorted(
        department_source["department"]
        .dropna()
        .unique()
        .tolist()
    ),
    default=sorted(
        department_source["department"]
        .dropna()
        .unique()
        .tolist()
    ),
)


selected_specialty = st.sidebar.multiselect(
    "Select Specialty",
    options=sorted(
        specialty_source["specialty"]
        .dropna()
        .unique()
        .tolist()
    ),
    default=sorted(
        specialty_source["specialty"]
        .dropna()
        .unique()
        .tolist()
    ),
)


selected_insurance = st.sidebar.multiselect(
    "Select Insurance Type",
    options=sorted(
        insurance_source["insurance_type"]
        .dropna()
        .unique()
        .tolist()
    ),
    default=sorted(
        insurance_source["insurance_type"]
        .dropna()
        .unique()
        .tolist()
    ),
)


st.sidebar.divider()

st.sidebar.info(
    "Each filter updates its matching chart. "
    "KPI cards show overall totals."
)


# --------------------------------------------------
# COMMON CHART STYLING
# --------------------------------------------------

def style_chart(fig, x_title, y_title):

    fig.update_layout(
        template="plotly",
        xaxis_title=x_title,
        yaxis_title=y_title,
        font=dict(size=12),
        margin=dict(
            l=25,
            r=25,
            t=65,
            b=60
        ),
        title_x=0.02,
        coloraxis_showscale=False,
        hoverlabel=dict(
            font_size=13
        ),
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        gridcolor="rgba(128,128,128,0.2)"
    )

    return fig


# --------------------------------------------------
# 1. APPOINTMENT OVERVIEW
# --------------------------------------------------

st.header("1. Appointment Overview")

appointment = data["appointment"].iloc[0]

total = int(
    appointment["total_appointments"]
)

attended = int(
    appointment["attended_appointments"]
)

no_shows = int(
    appointment["no_show_appointments"]
)

no_show_rate = float(
    appointment["no_show_rate_pct"]
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Appointments",
    f"{total:,}"
)

c2.metric(
    "Attended",
    f"{attended:,}"
)

c3.metric(
    "No-Shows",
    f"{no_shows:,}"
)

c4.metric(
    "No-Show Rate",
    f"{no_show_rate:.2f}%"
)


st.caption(
    "KPI cards represent all appointment records "
    "and are not changed by chart filters."
)

st.divider()


# --------------------------------------------------
# 2. APPOINTMENT NO-SHOW ANALYSIS
# --------------------------------------------------

st.header("2. Appointment No-Show Analysis")

left, right = st.columns(2)


# Department chart

with left:

    st.subheader(
        "No-Show Rate by Department"
    )

    department = data["department"].copy()

    department = department[
        department["department"].isin(
            selected_department
        )
    ]

    if department.empty:

        st.info(
            "Select at least one department "
            "to display this chart."
        )

    else:

        fig = px.bar(
            department,
            x="department",
            y="no_show_rate_pct",
            color="no_show_rate_pct",
            text="no_show_rate_pct",
            title="Department-wise No-Show Rate",
            color_continuous_scale="Blues",
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            cliponaxis=False,
        )

        fig = style_chart(
            fig,
            "Department",
            "No-Show Rate (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Specialty chart

with right:

    st.subheader(
        "No-Show Rate by Specialty"
    )

    specialty = data["specialty"].copy()

    specialty = specialty[
        specialty["specialty"].isin(
            selected_specialty
        )
    ]

    if specialty.empty:

        st.info(
            "Select at least one specialty "
            "to display this chart."
        )

    else:

        fig = px.bar(
            specialty,
            x="specialty",
            y="no_show_rate_pct",
            color="no_show_rate_pct",
            text="no_show_rate_pct",
            title="Specialty-wise No-Show Rate",
            color_continuous_scale="Teal",
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            cliponaxis=False,
        )

        fig = style_chart(
            fig,
            "Specialty",
            "No-Show Rate (%)"
        )

        fig.update_layout(
            xaxis_tickangle=-35
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Age and insurance charts

left, right = st.columns(2)


with left:

    st.subheader(
        "No-Show Rate by Age Group"
    )

    fig = px.bar(
        data["age"],
        x="patient_age_group",
        y="no_show_rate_pct",
        text="no_show_rate_pct",
        title="Age Group Comparison",
        color="no_show_rate_pct",
        color_continuous_scale="Sunset",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(
        fig,
        "Patient Age Group",
        "No-Show Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with right:

    st.subheader(
        "No-Show Rate by Insurance Type"
    )

    insurance = data["insurance"].copy()

    insurance = insurance[
        insurance["insurance_type"].isin(
            selected_insurance
        )
    ]

    if insurance.empty:

        st.info(
            "Select at least one insurance type "
            "to display this chart."
        )

    else:

        fig = px.bar(
            insurance,
            x="insurance_type",
            y="no_show_rate_pct",
            text="no_show_rate_pct",
            title="Insurance Type Comparison",
            color="no_show_rate_pct",
            color_continuous_scale="Viridis",
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            cliponaxis=False,
        )

        fig = style_chart(
            fig,
            "Insurance Type",
            "No-Show Rate (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Statistical finding

st.subheader("Statistical Finding")

st.info(
    "Specialty showed a statistically significant "
    "association with appointment no-show status "
    "(chi-square test, p = 0.000031). "
    "This indicates an association, not causation."
)

st.divider()


# --------------------------------------------------
# 3. PATIENT SATISFACTION ANALYSIS
# --------------------------------------------------

st.header("3. Patient Satisfaction Analysis")

satisfaction = data["satisfaction"].copy()


# Handle unnamed metric column

if "metric" not in satisfaction.columns:

    if "Unnamed: 0" in satisfaction.columns:

        satisfaction = satisfaction.rename(
            columns={
                "Unnamed: 0": "metric"
            }
        )

    else:

        satisfaction = satisfaction.rename(
            columns={
                satisfaction.columns[0]: "metric"
            }
        )


# Handle score column

if "score" not in satisfaction.columns:

    if "0" in satisfaction.columns:

        satisfaction = satisfaction.rename(
            columns={
                "0": "score"
            }
        )

    else:

        value_columns = [
            c for c in satisfaction.columns
            if c != "metric"
        ]

        if not value_columns:

            st.error(
                "The satisfaction summary CSV "
                "does not contain a score column."
            )

            st.stop()

        satisfaction = satisfaction.rename(
            columns={
                value_columns[0]: "score"
            }
        )


satisfaction["score"] = pd.to_numeric(
    satisfaction["score"],
    errors="coerce"
)

satisfaction = satisfaction.dropna(
    subset=["metric", "score"]
)


overall_row = satisfaction[
    satisfaction["metric"] == "overall_satisfaction"
]


if overall_row.empty:

    st.error(
        "Could not find overall_satisfaction "
        "in satisfaction_rating_summary.csv."
    )

    st.stop()


overall_score = float(
    overall_row.iloc[0]["score"]
)


# Satisfaction KPIs

c1, c2 = st.columns(2)

c1.metric(
    "Average Overall Satisfaction",
    f"{overall_score:.2f} / 5"
)

c2.metric(
    "Average Waiting Time",
    "91.43 minutes"
)


# Satisfaction charts

left, right = st.columns(2)


with left:

    st.subheader(
        "Average Satisfaction Ratings"
    )

    rating_data = satisfaction[
        satisfaction["metric"] != "overall_satisfaction"
    ]

    fig = px.bar(
        rating_data,
        x="metric",
        y="score",
        text="score",
        title="Rating Category Comparison",
        color="score",
        color_continuous_scale="Teal",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(
        fig,
        "Rating Category",
        "Average Score (out of 5)"
    )

    fig.update_layout(
        yaxis_range=[0, 5],
        xaxis_tickangle=-25
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with right:

    st.subheader(
        "Satisfaction by Hospital"
    )

    hospital = data["hospital"].copy()

    fig = px.bar(
        hospital,
        x="hospital",
        y="overall_satisfaction",
        text="overall_satisfaction",
        title="Hospital-wise Overall Satisfaction",
        color="overall_satisfaction",
        color_continuous_scale="Sunset",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(
        fig,
        "Hospital",
        "Overall Satisfaction (out of 5)"
    )

    fig.update_layout(
        yaxis_range=[0, 5]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.caption(
    "Satisfaction scores are descriptive averages. "
    "Hospital sample sizes should be considered "
    "when comparing results."
)

st.divider()


# --------------------------------------------------
# 4. RESOURCE UTILISATION DATA QUALITY
# --------------------------------------------------

st.header(
    "4. Resource Utilisation Data Quality"
)

quality = data["resource_quality"].copy()


issue_row = quality[
    quality["validation_check"]
    == "Records with at least one validation issue"
]


if issue_row.empty:

    st.warning(
        "The combined resource data-quality "
        "result was not found."
    )

else:

    affected = int(
        issue_row.iloc[0]["affected_records"]
    )

    percentage = float(
        issue_row.iloc[0]["percentage_of_records"]
    )


    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Resource Records",
        "400"
    )

    c2.metric(
        "Records with Issues",
        f"{affected:,}"
    )

    c3.metric(
        "Records with Issues (%)",
        f"{percentage:.2f}%"
    )


    chart_quality = quality[
        quality["validation_check"]
        != "Records with at least one validation issue"
    ].copy()


    fig = px.bar(
        chart_quality,
        x="validation_check",
        y="percentage_of_records",
        text="percentage_of_records",
        title="Resource Data Validation Issues",
        color="percentage_of_records",
        color_continuous_scale="Reds",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(
        fig,
        "Validation Check",
        "Affected Records (%)"
    )

    fig.update_layout(
        xaxis_tickangle=-25
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.warning(
        f"Resource utilisation metrics are not presented "
        f"as reliable KPIs because {percentage:.2f}% "
        f"of records have at least one validation issue. "
        "Source-data verification is required."
    )


st.divider()


# --------------------------------------------------
# 5. PROJECT LIMITATIONS
# --------------------------------------------------

st.header("5. Project Limitations")

st.markdown(
    """
    - The available datasets do not contain all seven patient funnel stages.
    - Complete funnel conversion and leakage calculations require
      additional journey-stage data.
    - Revenue impact modelling requires actual revenue and conversion
      information.
    - Resource utilisation figures require source-data verification.
    - Appointment and satisfaction results are based on the supplied
      datasets.
    """
)

st.divider()


# --------------------------------------------------
# FOOTER AND DATA NOTE
# --------------------------------------------------

st.caption(
    "Pristyn Care Health Analytics | Dashboard v1 | "
    "Developed using Python, Pandas, Streamlit and Plotly"
)


st.info(
    "Data note: Appointment analysis relates to the available "
    "healthcare appointment dataset. Patient satisfaction results "
    "come from a separate Sunrise dataset and should not be "
    "interpreted as Pristyn Care results. Resource utilisation "
    "data is subject to the validation limitations described above."
)
