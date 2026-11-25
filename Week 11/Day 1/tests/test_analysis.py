import pandas as pd
import pytest

from analysis import (
    load_data,
    analyze_sales,
    create_visualizations,
    save_report,
)


def sample_data():
    return pd.DataFrame({
        "Date": pd.to_datetime([
            "2026-01-05",
            "2026-02-05",
            "2026-03-05",
            "2026-04-05",
        ]),
        "Region": ["South", "North", "South", "East"],
        "Category": [
            "Electronics", "Grocery",
            "Electronics", "Clothing"
        ],
        "Sales": [10000, 5000, 15000, 7000],
        "Units Sold": [10, 25, 15, 14],
    })


def test_load_data():
    df = load_data()

    assert not df.empty
    assert "Sales" in df.columns
    assert df["Date"].is_monotonic_increasing


def test_load_data_missing_columns(tmp_path):
    file_path = tmp_path / "invalid.csv"
    pd.DataFrame({"Date": ["2026-01-01"]}).to_csv(
        file_path, index=False
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        load_data(file_path)


def test_load_data_negative_sales(tmp_path):
    file_path = tmp_path / "negative.csv"

    pd.DataFrame({
        "Date": ["2026-01-01"],
        "Region": ["South"],
        "Category": ["Grocery"],
        "Sales": [-100],
        "Units Sold": [5],
    }).to_csv(file_path, index=False)

    with pytest.raises(ValueError, match="cannot be negative"):
        load_data(file_path)


def test_analyze_sales():
    df = sample_data()

    region, category, monthly, insights = analyze_sales(df)

    assert insights["total_sales"] == 37000
    assert insights["total_units"] == 64
    assert insights["top_region"] == "South"
    assert insights["top_category"] == "Electronics"
    assert len(monthly) == 4


def test_create_visualizations(tmp_path):
    df = sample_data()
    region, category, monthly, _ = analyze_sales(df)

    charts = create_visualizations(
        region, category, monthly, tmp_path
    )

    assert len(charts) == 4

    for chart in charts:
        assert (tmp_path / chart).exists()


def test_save_report(tmp_path, monkeypatch):
    import analysis

    monkeypatch.setattr(analysis, "OUTPUT_DIR", tmp_path)

    df = sample_data()
    region, category, monthly, insights = analyze_sales(df)

    report_path = save_report(
        insights, region, category, monthly
    )

    assert report_path.exists()
    assert report_path.name == "storytelling_report.json"