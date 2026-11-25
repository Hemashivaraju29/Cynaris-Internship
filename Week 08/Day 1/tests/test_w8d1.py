import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import pytest
from pptx import Presentation

from executive_summary import calculate_insights
from ppt_export import export_presentation


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "Region": ["North", "South", "North", "South"],
        "Category": ["Electronics", "Grocery", "Clothing", "Grocery"],
        "Sales": [1000, 3000, 2000, 4000],
        "Units Sold": [10, 30, 20, 40],
    })


def test_calculate_five_insights(sample_df):
    insights = calculate_insights(sample_df)

    assert len(insights) == 5
    assert "4 rows and 5 columns" in insights[0]
    assert "Average Sales is 2,500.00" in insights[1]
    assert "Highest Sales is 4,000.00" in insights[2]
    assert "Lowest Sales is 1,000.00" in insights[3]
    assert "South region" in insights[4]
    assert "7,000.00" in insights[4]


def test_empty_dataframe_raises_error():
    with pytest.raises(ValueError, match="empty"):
        calculate_insights(pd.DataFrame())


def test_export_creates_seven_slide_presentation(tmp_path, sample_df):
    insights = calculate_insights(sample_df)
    summary = "Sales are growing. Focus on the strongest region."

    output_file = tmp_path / "executive_summary.pptx"
    export_presentation(insights, summary, str(output_file))

    assert output_file.exists()

    presentation = Presentation(str(output_file))
    assert len(presentation.slides) == 7


def test_export_requires_five_insights(tmp_path):
    output_file = tmp_path / "invalid.pptx"

    with pytest.raises(ValueError):
        export_presentation(["Only one insight"], "Summary", str(output_file))
