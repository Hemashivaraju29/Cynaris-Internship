import pandas as pd
import pytest

import executive_report as report


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Date": pd.to_datetime([
            "2026-01-05", "2026-02-05", "2026-03-05"
        ]),
        "Region": ["South", "North", "South"],
        "Category": ["Electronics", "Furniture", "Clothing"],
        "Sales": [10000, 15000, 20000],
        "Units Sold": [10, 15, 20],
    })


def test_load_data(monkeypatch, tmp_path):
    data = pd.DataFrame({
        "Date": ["2026-01-05"],
        "Region": ["South"],
        "Category": ["Electronics"],
        "Sales": [10000],
        "Units Sold": [10],
    })
    file_path = tmp_path / "sales.csv"
    data.to_csv(file_path, index=False)

    monkeypatch.setattr(report, "DATA_FILE", file_path)

    result = report.load_data()

    assert len(result) == 1
    assert result["Sales"].sum() == 10000


def test_load_data_missing_columns(monkeypatch, tmp_path):
    file_path = tmp_path / "invalid.csv"
    pd.DataFrame({"Date": ["2026-01-05"], "Sales": [100]}).to_csv(
        file_path, index=False
    )
    monkeypatch.setattr(report, "DATA_FILE", file_path)

    with pytest.raises(ValueError, match="Missing required columns"):
        report.load_data()


def test_analyse_data(sample_data):
    metrics = report.analyse_data(sample_data)

    assert metrics["total_sales"] == 45000
    assert metrics["average_sales"] == 15000
    assert metrics["total_units"] == 45
    assert metrics["transactions"] == 3
    assert metrics["regional"].idxmax() == "South"
    assert metrics["category"].idxmax() == "Clothing"


def test_create_plotly_charts(sample_data, monkeypatch, tmp_path):
    metrics = report.analyse_data(sample_data)
    chart_dir = tmp_path / "charts"
    monkeypatch.setattr(report, "CHART_DIR", chart_dir)

    report.create_plotly_charts(metrics)

    assert len(list(chart_dir.glob("*.html"))) == 3
    assert (chart_dir / "regional_sales.html").exists()
    assert (chart_dir / "category_sales.html").exists()
    assert (chart_dir / "monthly_sales.html").exists()


def test_create_powerpoint(sample_data, monkeypatch, tmp_path):
    metrics = report.analyse_data(sample_data)
    monkeypatch.setattr(report, "OUTPUT_DIR", tmp_path)

    output = report.create_powerpoint(metrics)

    assert output.exists()

    from pptx import Presentation
    presentation = Presentation(output)

    assert len(presentation.slides) == 5

    slide_text = [
        shape.text
        for slide in presentation.slides
        for shape in slide.shapes
        if shape.has_text_frame
    ]

    assert any("Executive Sales Report" in text for text in slide_text)
    assert any("Recommendations" in text for text in slide_text)
