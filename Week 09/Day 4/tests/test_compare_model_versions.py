import pandas as pd


def get_metric(metrics, name):
    return metrics.get(name.lower(), metrics.get(name.upper()))


def test_metric_lookup_supports_uppercase():
    metrics = {"MAE": 4753.09, "RMSE": 6929.94, "R2": 0.0172}

    assert get_metric(metrics, "mae") == 4753.09
    assert get_metric(metrics, "rmse") == 6929.94
    assert get_metric(metrics, "r2") == 0.0172


def test_metric_lookup_supports_lowercase():
    metrics = {"mae": 100.0, "rmse": 200.0, "r2": 0.8}

    assert get_metric(metrics, "mae") == 100.0
    assert get_metric(metrics, "rmse") == 200.0
    assert get_metric(metrics, "r2") == 0.8


def test_comparison_versions_are_sorted():
    comparison = pd.DataFrame({"version": [3, 1, 2]})

    comparison = comparison.sort_values("version")

    assert list(comparison["version"]) == [1, 2, 3]