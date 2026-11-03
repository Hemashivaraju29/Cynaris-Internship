
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Healthcare Analytics Demo",
    page_icon="📊",
    layout="wide"
)

# ---------------- PAGE DESIGN ----------------

st.markdown("""
<style>
.block-container {
    padding: 2rem 3rem;
    max-width: 1500px;
}
h1 {color: #123B5D;}
h2 {color: #176B87;}
[data-testid="stMetric"] {
    background-color: #F0F5F9;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #D9E4EC;
}
</style>
""", unsafe_allow_html=True)

st.title("Healthcare Analytics Dashboard")
st.caption("Dashboard v1 | Synthetic Demonstration Data")

st.warning(
    "DEMO ONLY: All figures on this dashboard are synthetic "
    "and do not represent actual patients, hospitals, or business results."
)

# ---------------- SYNTHETIC DATA ----------------

appointment = pd.DataFrame([{
    "total": 2000,
    "attended": 1680,
    "no_shows": 320
}])

appointment["no_show_rate"] = (
    appointment["no_shows"] / appointment["total"] * 100
)

department = pd.DataFrame({
    "department": ["OPD", "Emergency", "Cardiology", "Specialist Clinic"],
    "appointments": [500, 450, 400, 650],
    "no_shows": [65, 90, 48, 117]
})
department["no_show_rate"] = (
    department["no_shows"] / department["appointments"] * 100
)

specialty = pd.DataFrame({
    "specialty": [
        "General Medicine", "Dermatology", "ENT",
        "Orthopedics", "Cardiology"
    ],
    "no_show_rate": [22.5, 20.4, 17.7, 12.6, 9.5]
})

age = pd.DataFrame({
    "age_group": ["0-18", "19-35", "36-50", "51-65", "65+"],
    "no_show_rate": [19.2, 18.2, 14.5, 13.2, 15.9]
})

insurance = pd.DataFrame({
    "insurance_type": ["Self-pay", "Government", "Private", "Corporate"],
    "no_show_rate": [17.7, 15.8, 15.7, 15.5]
})

satisfaction = pd.DataFrame({
    "rating": ["Doctor", "Nurse", "Cleanliness", "Billing", "Overall"],
    "score": [4.1, 4.2, 4.0, 3.8, 4.1]
})

hospital = pd.DataFrame({
    "hospital": ["Hospital A", "Hospital B", "Hospital C", "Hospital D"],
    "satisfaction": [3.8, 4.0, 4.2, 4.1]
})

resource = pd.DataFrame({
    "department": ["OPD", "Emergency", "Cardiology", "Surgery"],
    "bed_occupancy": [72, 85, 68, 78],
    "resource_utilisation": [75, 88, 70, 81]
})

quality = pd.DataFrame({
    "metric": ["Valid records", "Records needing review"],
    "records": [920, 80]
})

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.title("Dashboard Filters")

selected_departments = st.sidebar.multiselect(
    "Select Department",
    department["department"].tolist(),
    default=department["department"].tolist()
)

st.sidebar.info("All displayed data is synthetic demonstration data.")

# ---------------- 1. APPOINTMENT OVERVIEW ----------------

st.header("1. Appointment Overview")

row = appointment.iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Appointments", f"{row['total']:,}")
c2.metric("Attended", f"{row['attended']:,}")
c3.metric("No-Shows", f"{row['no_shows']:,}")
c4.metric("No-Show Rate", f"{row['no_show_rate']:.2f}%")

st.divider()

# ---------------- 2. NO-SHOW ANALYSIS ----------------

st.header("2. Appointment No-Show Analysis")

filtered_department = department[
    department["department"].isin(selected_departments)
]

left, right = st.columns(2)

with left:
    st.subheader("No-Show Rate by Department")

    if not filtered_department.empty:
        fig = px.bar(
            filtered_department,
            x="department",
            y="no_show_rate",
            text="no_show_rate",
            title="Department-wise No-Show Rate"
        )
        fig.update_traces(texttemplate="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one department.")

with right:
    st.subheader("No-Show Rate by Specialty")

    fig = px.bar(
        specialty,
        x="specialty",
        y="no_show_rate",
        title="Specialty-wise No-Show Rate"
    )
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("No-Show Rate by Age Group")
    fig = px.bar(age, x="age_group", y="no_show_rate")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("No-Show Rate by Insurance Type")
    fig = px.bar(insurance, x="insurance_type", y="no_show_rate")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- 3. PATIENT SATISFACTION ----------------

st.header("3. Patient Satisfaction Analysis")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Average Satisfaction Ratings")
    fig = px.bar(
        satisfaction,
        x="rating",
        y="score",
        range_y=[0, 5],
        title="Satisfaction by Category"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Satisfaction by Hospital")
    fig = px.bar(
        hospital,
        x="hospital",
        y="satisfaction",
        range_y=[0, 5],
        title="Hospital-wise Satisfaction"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- 4. RESOURCE UTILISATION ----------------

st.header("4. Resource Utilisation")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Bed Occupancy")
    fig = px.bar(
        resource,
        x="department",
        y="bed_occupancy",
        range_y=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Resource Utilisation")
    fig = px.bar(
        resource,
        x="department",
        y="resource_utilisation",
        range_y=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Demo Data Quality Summary")

fig = px.pie(
    quality,
    names="metric",
    values="records",
    title="Synthetic Data Validation"
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- 5. SUMMARY ----------------

st.header("5. Key Observations")

st.markdown("""
- The synthetic appointment dataset demonstrates how attendance
  and no-show KPIs can be monitored.
- Department and specialty charts help identify areas for further review.
- Satisfaction charts compare different service categories.
- Resource charts demonstrate bed occupancy and resource utilisation.
- Data-quality indicators help highlight records requiring review.

These observations are illustrative and are not findings from a real
healthcare organisation.
""")

st.success("Synthetic healthcare analytics dashboard loaded successfully.")

st.caption(
    "Healthcare Analytics Demo | Python, Pandas, Streamlit and Plotly"
)
