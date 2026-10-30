
import pandas as pd
from scipy.stats import chi2_contingency


def test_conversion_rate_calculation():
    data = pd.DataFrame({
        "group": ["A", "A", "B", "B"],
        "visitors": [100, 100, 100, 100],
        "conversions": [10, 20, 15, 25]
    })

    summary = data.groupby("group")[["visitors", "conversions"]].sum()
    summary["conversion_rate"] = (
        summary["conversions"] / summary["visitors"]
    )

    assert summary.loc["A", "conversion_rate"] == 0.15
    assert summary.loc["B", "conversion_rate"] == 0.20


def test_chi_square_result():
    observed = [[113, 1022], [169, 966]]

    chi2, p_value, dof, expected = chi2_contingency(observed)

    assert chi2 > 0
    assert 0 <= p_value <= 1
    assert p_value < 0.05
