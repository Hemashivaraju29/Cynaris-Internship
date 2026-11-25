-- 1. Total appointments
SELECT
    COUNT(*) AS total_appointments
FROM healthcare_appointments;

-- 2. Attended appointments
SELECT
    COUNT(*) AS attended_appointments
FROM healthcare_appointments
WHERE no_show = 0;

-- 3. No-show appointments
SELECT
    COUNT(*) AS no_show_appointments
FROM healthcare_appointments
WHERE no_show = 1;

-- 4. Overall no-show rate
SELECT
    ROUND(
        SUM(CASE WHEN no_show = 1 THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2
    ) AS no_show_rate_pct
FROM healthcare_appointments;

-- 5. No-show rate by department
SELECT
    department,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN no_show = 1 THEN 1 ELSE 0 END) AS no_shows,
    ROUND(
        SUM(CASE WHEN no_show = 1 THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2
    ) AS no_show_rate_pct
FROM healthcare_appointments
GROUP BY department
ORDER BY no_show_rate_pct DESC;

-- 6. No-show rate by specialty
SELECT
    specialty,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN no_show = 1 THEN 1 ELSE 0 END) AS no_shows,
    ROUND(
        SUM(CASE WHEN no_show = 1 THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2
    ) AS no_show_rate_pct
FROM healthcare_appointments
GROUP BY specialty
ORDER BY no_show_rate_pct DESC;
-- 7. Average patient satisfaction ratings
SELECT
    ROUND(AVG(doctor_rating), 2) AS avg_doctor_rating,
    ROUND(AVG(nurse_rating), 2) AS avg_nurse_rating,
    ROUND(AVG(cleanliness_rating), 2) AS avg_cleanliness_rating,
    ROUND(AVG(billing_clarity_rating), 2) AS avg_billing_rating,
    ROUND(AVG(overall_satisfaction), 2) AS avg_overall_satisfaction
FROM patient_satisfaction;

-- 8. Satisfaction by hospital
SELECT
    hospital,
    COUNT(*) AS total_surveys,
    ROUND(AVG(overall_satisfaction), 2) AS avg_satisfaction
FROM patient_satisfaction
GROUP BY hospital
ORDER BY avg_satisfaction DESC;

-- 9. Patient recommendation responses
SELECT
    would_recommend,
    COUNT(*) AS response_count
FROM patient_satisfaction
GROUP BY would_recommend;

-- 10. Resource data quality checks
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN occupied_beds > total_beds THEN 1 ELSE 0 END)
        AS invalid_bed_records,
    SUM(CASE WHEN icu_beds_occupied > icu_beds_total THEN 1 ELSE 0 END)
        AS invalid_icu_records,
    SUM(CASE WHEN surgeries_completed > surgeries_scheduled THEN 1 ELSE 0 END)
        AS invalid_surgery_records
FROM resource_utilisation;