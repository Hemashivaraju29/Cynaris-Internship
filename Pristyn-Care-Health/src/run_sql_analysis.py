import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "outputs" / "pristyn_healthcare.db"

queries = {
    "Overall Appointment Summary": """
        SELECT
            COUNT(*) AS total_appointments,
            SUM(CASE WHEN no_show = 0 THEN 1 ELSE 0 END) AS attended,
            SUM(CASE WHEN no_show = 1 THEN 1 ELSE 0 END) AS no_shows,
            ROUND(AVG(no_show) * 100, 2) AS no_show_rate_pct
        FROM healthcare_appointments;
    """,

    "No-show Rate by Department": """
        SELECT department,
               COUNT(*) AS total_appointments,
               SUM(no_show) AS no_shows,
               ROUND(AVG(no_show) * 100, 2) AS no_show_rate_pct
        FROM healthcare_appointments
        GROUP BY department
        ORDER BY no_show_rate_pct DESC;
    """,

    "No-show Rate by Specialty": """
        SELECT specialty,
               COUNT(*) AS total_appointments,
               SUM(no_show) AS no_shows,
               ROUND(AVG(no_show) * 100, 2) AS no_show_rate_pct
        FROM healthcare_appointments
        GROUP BY specialty
        ORDER BY no_show_rate_pct DESC;
    """,

    "Patient Satisfaction Ratings": """
        SELECT
            ROUND(AVG(doctor_rating), 2) AS avg_doctor_rating,
            ROUND(AVG(nurse_rating), 2) AS avg_nurse_rating,
            ROUND(AVG(cleanliness_rating), 2) AS avg_cleanliness_rating,
            ROUND(AVG(billing_clarity_rating), 2) AS avg_billing_rating,
            ROUND(AVG(overall_satisfaction), 2) AS avg_overall_satisfaction
        FROM patient_satisfaction;
    """,

    "Satisfaction by Hospital": """
        SELECT hospital,
               COUNT(*) AS total_surveys,
               ROUND(AVG(overall_satisfaction), 2) AS avg_satisfaction
        FROM patient_satisfaction
        GROUP BY hospital
        ORDER BY avg_satisfaction DESC;
    """,

    "Patient Recommendation Responses": """
        SELECT would_recommend,
               COUNT(*) AS response_count
        FROM patient_satisfaction
        GROUP BY would_recommend;
    """,

    "Resource Data Quality Checks": """
        SELECT
            COUNT(*) AS total_records,
            SUM(CASE WHEN occupied_beds > total_beds THEN 1 ELSE 0 END)
                AS invalid_bed_records,
            SUM(CASE WHEN icu_beds_occupied > icu_beds_total THEN 1 ELSE 0 END)
                AS invalid_icu_records,
            SUM(CASE WHEN surgeries_completed > surgeries_scheduled THEN 1 ELSE 0 END)
                AS invalid_surgery_records
        FROM resource_utilisation;
    """
}

with sqlite3.connect(DB_PATH) as connection:
    for title, query in queries.items():
        print(f"\n{'=' * 55}")
        print(title)
        print('=' * 55)

        cursor = connection.execute(query)
        print(" | ".join(column[0] for column in cursor.description))

        for row in cursor.fetchall():
            print(row)