
import pandas as pd
import pytest

from experiment_pipeline import calculate_metrics, load_dataset


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Date": ["2026-01-05", "2026-01-12", "2026-01-05"],
        "Region": ["North", "South", "North"],
        "Category": ["Electronics", "Grocery", "Electronics"],
        "Sales": [10000, 5000, 10000],
        "Units Sold": [20, 50, 20],
    })


def test_calculate_metrics(sample_data):
    metrics = calculate_metrics(sample_data)

    assert metrics["rows"] == 3
    assert metrics["columns"] == 5
    assert metrics["missing_cells"] == 0
    assert metrics["duplicate_rows"] == 1
    assert metrics["total_sales"] == 25000
    assert metrics["average_sales"] == pytest.approx(25000 / 3)
    assert metrics["maximum_sales"] == 10000
    assert metrics["minimum_sales"] == 5000
    assert metrics["total_units_sold"] == 90


def test_load_dataset():
    df = load_dataset()

    assert len(df) == 24
    assert list(df.columns) == [
        "Date", "Region", "Category", "Sales", "Units Sold"
    ]


def test_load_dataset_missing_file():
    with pytest.raises(FileNotFoundError):
        load_dataset("missing_dataset.csv")


def test_load_dataset_missing_columns(tmp_path):
    invalid_file = tmp_path / "invalid.csv"
    pd.DataFrame({"Date": ["2026-01-05"]}).to_csv(
        invalid_file, index=False
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        load_dataset(invalid_file)
