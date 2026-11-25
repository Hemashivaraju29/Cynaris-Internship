
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# CUSTOM CSS - LIGHT AND DARK MODE SUPPORT
# ============================================================

st.markdown("""
<style>
.block-container {
    padding: 2rem 3rem;
    max-width: 1500px;
}

h1 {
    font-weight: 750;
}

h2 {
    font-weight: 650;
}

h3 {
    font-weight: 600;
}

/* Theme-aware KPI cards */
[data-testid="stMetric"] {
    background: var(--secondary-background-color);
    color: var(--text-color);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    min-width: 0;
    overflow-wrap: anywhere;
}

[data-testid="stMetricLabel"] {
    color: var(--text-color) !important;
    font-size: 14px;
}

[data-testid="stMetricValue"] {
    color: var(--text-color) !important;
    font-size: clamp(20px, 2vw, 30px);
    font-weight: 750;
}

[data-testid="stMetricDelta"] {
    color: var(--text-color) !important;
}

/* Section spacing */
[data-testid="stVerticalBlock"] > div {
    min-width: 0;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("📊 Healthcare Analytics Dashboard")

st.caption(
    "Dashboard v2 | Appointment Analysis, "
    "Patient Satisfaction and Resource Utilisation"
)

st.warning(
    "DEMO ONLY: All figures displayed on this dashboard "
    "are synthetic demonstration data. They do not represent "
    "actual patients, hospitals, or business results."
)

# ============================================================
# SYNTHETIC DATA
# ============================================================

# Appointment overview
appointment = pd.DataFrame([{
    "total": 2000,
    "attended": 1680,
    "no_shows": 320
}])

appointment["no_show_rate"] = (
    appointment["no_shows"] /
    appointment["total"] * 100
)

# Department analysis
department = pd.DataFrame({
    "department": [
        "OPD",
        "Emergency",
        "Cardiology",
        "Specialist Clinic"
    ],
    "appointments": [500, 450, 400, 650],
    "no_shows": [65, 90, 48, 117]
})

department["no_show_rate"] = (
    department["no_shows"] /
    department["appointments"] * 100
)

# Specialty analysis
specialty = pd.DataFrame({
    "specialty": [
        "General Medicine",
        "Dermatology",
        "ENT",
        "Orthopedics",
        "Cardiology"
    ],
    "no_show_rate": [
        22.5, 20.4, 17.7, 12.6, 9.5
    ]
})

# Age-group analysis
age = pd.DataFrame({
    "age_group": [
        "0-18",
        "19-35",
        "36-50",
        "51-65",
        "65+"
    ],
    "no_show_rate": [
        19.2, 18.2, 14.5, 13.2, 15.9
    ]
})

# Insurance analysis
insurance = pd.DataFrame({
    "insurance_type": [
        "Self-pay",
        "Government",
        "Private",
        "Corporate"
    ],
    "no_show_rate": [
        17.7, 15.8, 15.7, 15.5
    ]
})

# Patient satisfaction
satisfaction = pd.DataFrame({
    "rating": [
        "Doctor",
        "Nurse",
        "Cleanliness",
        "Billing",
        "Overall"
    ],
    "score": [
        4.1, 4.2, 4.0, 3.8, 4.1
    ]
})

# Hospital satisfaction
hospital = pd.DataFrame({
    "hospital": [
        "Hospital A",
        "Hospital B",
        "Hospital C",
        "Hospital D"
    ],
    "satisfaction": [
        3.8, 4.0, 4.2, 4.1
    ]
})

# Resource utilisation
resource = pd.DataFrame({
    "department": [
        "OPD",
        "Emergency",
        "Cardiology",
        "Surgery"
    ],
    "bed_occupancy": [
        72, 85, 68, 78
    ],
    "resource_utilisation": [
        75, 88, 70, 81
    ]
})

# Synthetic data-quality summary
quality = pd.DataFrame({
    "metric": [
        "Valid records",
        "Records needing review"
    ],
    "records": [
        920, 80
    ]
})

# ============================================================
# PLOTLY CHART HELPER
# ============================================================

def format_chart(fig, y_title=None):
    """Apply consistent, readable formatting to charts."""

    fig.update_layout(
        template="plotly",
        autosize=True,
        title_x=0.02,
        margin=dict(l=20, r=20, t=65, b=50),
        font=dict(size=13),
        xaxis_title=None,
        yaxis_title=y_title,
        legend_title_text="",
        hoverlabel=dict(
            font_size=13
        )
    )

    fig.update_xaxes(
        automargin=True,
        tickangle=-20
    )

    fig.update_yaxes(
        automargin=True,
        rangemode="tozero"
    )

    return fig


def create_bar_chart(
    df,
    x,
    y,
    title,
    color_column,
    palette,
    y_title,
    percentage=False,
    y_range=None
):
    """Create a consistently formatted coloured bar chart."""

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color_column,
        color_discrete_sequence=palette,
        text=y,
        title=title,
        hover_data={y: ":.2f"}
    )

    if percentage:
        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            cliponaxis=False
        )
    else:
        fig.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            cliponaxis=False
        )

    format_chart(fig, y_title)

    if y_range:
        fig.update_yaxes(range=y_range)

    return fig


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("Dashboard Filters")

st.sidebar.caption(
    "Use the filters to explore appointment data."
)

selected_departments = st.sidebar.multiselect(
    "Select Department",
    options=department["department"].tolist(),
    default=department["department"].tolist()
)

st.sidebar.divider()

st.sidebar.info(
    "All figures on this dashboard are synthetic "
    "demonstration data."
)

# ============================================================
# 1. APPOINTMENT OVERVIEW
# ============================================================

st.header("1. Appointment Overview")

row = appointment.iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Appointments",
    f"{row['total']:,}"
)

c2.metric(
    "Attended",
    f"{row['attended']:,}"
)

c3.metric(
    "No-Shows",
    f"{row['no_shows']:,}"
)

c4.metric(
    "No-Show Rate",
    f"{row['no_show_rate']:.2f}%"
)

st.caption(
    "These KPI cards represent the complete synthetic "
    "appointment dataset."
)

st.divider()

# ============================================================
# 2. APPOINTMENT NO-SHOW ANALYSIS
# ============================================================

st.header("2. Appointment No-Show Analysis")

left, right = st.columns(2)

# Department chart
with left:

    st.subheader("No-Show Rate by Department")

    filtered_department = department[
        department["department"].isin(
            selected_departments
        )
    ]

    if not filtered_department.empty:

        fig = create_bar_chart(
            filtered_department,
            x="department",
            y="no_show_rate",
            title="Department-wise No-Show Rate",
            color_column="department",
            palette=px.colors.qualitative.Set2,
            y_title="No-Show Rate (%)",
            percentage=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info(
            "Select at least one department to display this chart."
        )

# Specialty chart
with right:

    st.subheader("No-Show Rate by Specialty")

    fig = create_bar_chart(
        specialty,
        x="specialty",
        y="no_show_rate",
        title="Specialty-wise No-Show Rate",
        color_column="specialty",
        palette=px.colors.qualitative.Bold,
        y_title="No-Show Rate (%)",
        percentage=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Age and insurance charts
left, right = st.columns(2)

with left:

    st.subheader("No-Show Rate by Age Group")

    fig = create_bar_chart(
        age,
        x="age_group",
        y="no_show_rate",
        title="Age-wise No-Show Rate",
        color_column="age_group",
        palette=px.colors.qualitative.Set2,
        y_title="No-Show Rate (%)",
        percentage=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("No-Show Rate by Insurance Type")

    fig = create_bar_chart(
        insurance,
        x="insurance_type",
        y="no_show_rate",
        title="Insurance-wise No-Show Rate",
        color_column="insurance_type",
        palette=px.colors.qualitative.Pastel,
        y_title="No-Show Rate (%)",
        percentage=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ============================================================
# 3. PATIENT SATISFACTION
# ============================================================

st.header("3. Patient Satisfaction Analysis")

left, right = st.columns(2)

with left:

    st.subheader("Average Satisfaction Ratings")

    fig = create_bar_chart(
        satisfaction,
        x="rating",
        y="score",
        title="Satisfaction by Category",
        color_column="rating",
        palette=px.colors.qualitative.Safe,
        y_title="Satisfaction Score",
        y_range=[0, 5]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Satisfaction by Hospital")

    fig = create_bar_chart(
        hospital,
        x="hospital",
        y="satisfaction",
        title="Hospital-wise Satisfaction",
        color_column="hospital",
        palette=px.colors.qualitative.Vivid,
        y_title="Satisfaction Score",
        y_range=[0, 5]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ============================================================
# 4. RESOURCE UTILISATION
# ============================================================

st.header("4. Resource Utilisation")

left, right = st.columns(2)

with left:

    st.subheader("Bed Occupancy")

    fig = px.bar(
        resource,
        x="department",
        y="bed_occupancy",
        color="bed_occupancy",
        color_continuous_scale="Teal",
        text="bed_occupancy",
        title="Department-wise Bed Occupancy"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )

    format_chart(
        fig,
        "Bed Occupancy (%)"
    )

    fig.update_yaxes(
        range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Resource Utilisation")

    fig = px.bar(
        resource,
        x="department",
        y="resource_utilisation",
        color="resource_utilisation",
        color_continuous_scale="Sunset",
        text="resource_utilisation",
        title="Department-wise Resource Utilisation"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )

    format_chart(
        fig,
        "Resource Utilisation (%)"
    )

    fig.update_yaxes(
        range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# 5. DATA QUALITY SUMMARY
# ============================================================

st.subheader("Synthetic Data Quality Summary")

fig = px.pie(
    quality,
    names="metric",
    values="records",
    title="Synthetic Data Validation",
    color="metric",
    color_discrete_sequence=px.colors.qualitative.Set1,
    hole=0.35
)

fig.update_traces(
    textposition="inside",
    textinfo="label+percent",
    hovertemplate="%{label}: %{value}<extra></extra>"
)

fig.update_layout(
    template="plotly",
    title_x=0.02,
    margin=dict(l=20, r=20, t=65, b=30)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ============================================================
# 6. KEY OBSERVATIONS
# ============================================================

st.header("5. Key Observations")

st.markdown("""
- The synthetic appointment dataset demonstrates how
  attendance and no-show KPIs can be monitored.
- Department and specialty charts help identify areas
  that may need further investigation.
- Satisfaction charts compare different service categories.
- Resource charts demonstrate bed occupancy and
  resource utilisation.
- Data-quality indicators demonstrate how records
  requiring review can be monitored.
""")

st.info(
    "These observations are illustrative only. "
    "They are not findings from a real healthcare organisation."
)

# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Healthcare Analytics Dashboard | "
    "Built using Python, Pandas, Streamlit and Plotly | "
    "Synthetic Demonstration Version"
)
