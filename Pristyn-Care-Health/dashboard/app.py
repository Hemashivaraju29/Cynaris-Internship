from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Pristyn Care | Healthcare Analytics", page_icon="🏥", layout="wide")

st.markdown("""
<style>
.block-container {padding: 2rem 3rem; max-width: 1500px;}
h1 {color: #123B5D; font-weight: 700;}
h2 {color: #176B87; font-weight: 600;}
[data-testid="stMetric"] {
    background-color: #F0F5F9; padding: 18px; border-radius: 10px;
    border: 1px solid #D9E4EC;
}
[data-testid="stMetricValue"] {color: #123B5D;}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

st.title("🏥 Pristyn Care Health Analytics Dashboard")
st.caption("Dashboard v1 | Appointment, Patient Satisfaction and Data Quality")


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
            raise FileNotFoundError(f"Missing required file: {path}")
        result[key] = pd.read_csv(path)
    return result


try:
    data = load_data()
except Exception as error:
    st.error(f"Unable to load dashboard data: {error}")
    st.info("Run the project analysis scripts to generate the required CSV files.")
    st.stop()


# SIDEBAR FILTERS
st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Explore appointment records")

department_source = data["department"]
specialty_source = data["specialty"]
insurance_source = data["insurance"]

selected_department = st.sidebar.multiselect(
    "Select Department",
    options=sorted(department_source["department"].dropna().unique().tolist()),
    default=sorted(department_source["department"].dropna().unique().tolist()),
)
selected_specialty = st.sidebar.multiselect(
    "Select Specialty",
    options=sorted(specialty_source["specialty"].dropna().unique().tolist()),
    default=sorted(specialty_source["specialty"].dropna().unique().tolist()),
)
selected_insurance = st.sidebar.multiselect(
    "Select Insurance Type",
    options=sorted(insurance_source["insurance_type"].dropna().unique().tolist()),
    default=sorted(insurance_source["insurance_type"].dropna().unique().tolist()),
)
st.sidebar.divider()
st.sidebar.info("Each filter updates its matching chart. KPI cards show overall totals.")


# 1. APPOINTMENT OVERVIEW
st.header("1. Appointment Overview")
appointment = data["appointment"].iloc[0]
total = int(appointment["total_appointments"])
attended = int(appointment["attended_appointments"])
no_shows = int(appointment["no_show_appointments"])
no_show_rate = float(appointment["no_show_rate_pct"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Appointments", f"{total:,}")
c2.metric("Attended", f"{attended:,}")
c3.metric("No-Shows", f"{no_shows:,}")
c4.metric("No-Show Rate", f"{no_show_rate:.2f}%")
st.caption("KPI cards represent all appointment records and are not changed by chart filters.")
st.divider()


# 2. APPOINTMENT NO-SHOW ANALYSIS
st.header("2. Appointment No-Show Analysis")
left, right = st.columns(2)

with left:
    st.subheader("No-Show Rate by Department")
    department = data["department"].copy()
    department = department[department["department"].isin(selected_department)]
    if department.empty:
        st.info("Select at least one department to display this chart.")
    else:
        fig = px.bar(
            department, x="department", y="no_show_rate_pct",
            color="no_show_rate_pct", text="no_show_rate_pct",
            title="Department-wise No-Show Rate", color_continuous_scale="Blues",
        )
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_layout(
            yaxis_title="No-Show Rate (%)", xaxis_title="Department",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("No-Show Rate by Specialty")
    specialty = data["specialty"].copy()
    specialty = specialty[specialty["specialty"].isin(selected_specialty)]
    if specialty.empty:
        st.info("Select at least one specialty to display this chart.")
    else:
        fig = px.bar(
            specialty, x="specialty", y="no_show_rate_pct",
            color="no_show_rate_pct", text="no_show_rate_pct",
            title="Specialty-wise No-Show Rate", color_continuous_scale="Blues",
        )
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_layout(
            yaxis_title="No-Show Rate (%)", xaxis_title="Specialty",
            xaxis_tickangle=-35, coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("No-Show Rate by Age Group")
    fig = px.bar(
        data["age"], x="patient_age_group", y="no_show_rate_pct",
        text="no_show_rate_pct", title="Age Group Comparison",
        color="no_show_rate_pct", color_continuous_scale="Blues",
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(
        yaxis_title="No-Show Rate (%)", xaxis_title="Patient Age Group",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("No-Show Rate by Insurance Type")
    insurance = data["insurance"].copy()
    insurance = insurance[insurance["insurance_type"].isin(selected_insurance)]
    if insurance.empty:
        st.info("Select at least one insurance type to display this chart.")
    else:
        fig = px.bar(
            insurance, x="insurance_type", y="no_show_rate_pct",
            text="no_show_rate_pct", title="Insurance Type Comparison",
            color="no_show_rate_pct", color_continuous_scale="Blues",
        )
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_layout(
            yaxis_title="No-Show Rate (%)", xaxis_title="Insurance Type",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Statistical Finding")
st.info(
    "Specialty showed a statistically significant association with appointment "
    "no-show status (chi-square test, p = 0.000031). This indicates an association, not causation."
)
st.divider()


# 3. PATIENT SATISFACTION
st.header("3. Patient Satisfaction Analysis")
satisfaction = data["satisfaction"].copy()

# Handle the CSV format where metric names are stored in an unnamed first column.
if "metric" not in satisfaction.columns:
    if "Unnamed: 0" in satisfaction.columns:
        satisfaction = satisfaction.rename(columns={"Unnamed: 0": "metric"})
    else:
        satisfaction = satisfaction.rename(columns={satisfaction.columns[0]: "metric"})

if "score" not in satisfaction.columns:
    if "0" in satisfaction.columns:
        satisfaction = satisfaction.rename(columns={"0": "score"})
    else:
        value_columns = [c for c in satisfaction.columns if c != "metric"]
        if not value_columns:
            st.error("The satisfaction summary CSV does not contain a score column.")
            st.stop()
        satisfaction = satisfaction.rename(columns={value_columns[0]: "score"})

satisfaction["score"] = pd.to_numeric(satisfaction["score"], errors="coerce")
satisfaction = satisfaction.dropna(subset=["metric", "score"])
overall_row = satisfaction[satisfaction["metric"] == "overall_satisfaction"]
if overall_row.empty:
    st.error("Could not find overall_satisfaction in satisfaction_rating_summary.csv.")
    st.stop()
overall_score = float(overall_row.iloc[0]["score"])

c1, c2 = st.columns(2)
c1.metric("Average Overall Satisfaction", f"{overall_score:.2f} / 5")
c2.metric("Average Waiting Time", "91.43 minutes")

left, right = st.columns(2)
with left:
    st.subheader("Average Satisfaction Ratings")
    rating_data = satisfaction[satisfaction["metric"] != "overall_satisfaction"]
    fig = px.bar(
        rating_data, x="metric", y="score", text="score",
        title="Rating Category Comparison", color="score",
        color_continuous_scale="Blues",
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(
        yaxis_range=[0, 5], xaxis_tickangle=-25,
        yaxis_title="Average Score (out of 5)", xaxis_title="Rating Category",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    with right:st.subheader("Satisfaction by Hospital")
hospital = data["hospital"].copy()
fig = px.bar(
        hospital, x="hospital", y="overall_satisfaction",
        text="overall_satisfaction", title="Hospital-wise Overall Satisfaction",
        color="overall_satisfaction", color_continuous_scale="Blues",
    )
fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig.update_layout(
        yaxis_range=[0, 5], yaxis_title="Overall Satisfaction (out of 5)",
        xaxis_title="Hospital", coloraxis_showscale=False,
    )
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Satisfaction scores are descriptive averages. Hospital sample sizes should be considered when comparing results."
)
st.divider()


# 4. RESOURCE DATA QUALITY
st.header("4. Resource Utilisation Data Quality")
quality = data["resource_quality"].copy()
issue_row = quality[
    quality["validation_check"] == "Records with at least one validation issue"
]

if issue_row.empty:
    st.warning("The combined resource data-quality result was not found.")
else:
    affected = int(issue_row.iloc[0]["affected_records"])
    percentage = float(issue_row.iloc[0]["percentage_of_records"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Resource Records", "400")
    c2.metric("Records with Issues", f"{affected:,}")
    c3.metric("Records with Issues (%)", f"{percentage:.2f}%")

    chart_quality = quality[
        quality["validation_check"] != "Records with at least one validation issue"
    ].copy()
    fig = px.bar(
        chart_quality, x="validation_check", y="percentage_of_records",
        text="percentage_of_records", title="Resource Data Validation Issues",
        color="percentage_of_records", color_continuous_scale="Blues",
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(
        xaxis_title="Validation Check", yaxis_title="Affected Records (%)",
        xaxis_tickangle=-25, coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.warning(
        f"Resource utilisation metrics are not presented as reliable KPIs because "
        f"{percentage:.2f}% of records have at least one validation issue. "
        "Source-data verification is required."
    )
st.divider()


# 5. PROJECT LIMITATIONS
st.header("5. Project Limitations")
st.markdown("""
- The available datasets do not contain all seven patient funnel stages.
- Complete funnel conversion and leakage calculations require additional journey-stage data.
- Revenue impact modelling requires actual revenue and conversion information.
- Resource utilisation figures require source-data verification.
- Appointment and satisfaction results are based on the supplied datasets.
""")
st.divider()

st.caption(
    "Pristyn Care Health Analytics | Dashboard v1 | "
    "Developed using Python, Pandas, Streamlit and Plotly"
)
st.info(
    "Data note: Appointment analysis relates to the available healthcare "
    "appointment dataset. Patient satisfaction results come from a separate "
    "Sunrise dataset and should not be interpreted as Pristyn Care results. "
    "Resource utilisation data is subject to the validation limitations "
    "described below."
)
