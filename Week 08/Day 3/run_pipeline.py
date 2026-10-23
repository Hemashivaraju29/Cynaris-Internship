import argparse
from pathlib import Path
import sys

import pandas as pd

# Allow imports from this day's folder when the script is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from business_recommendations import (
    calculate_insights,
    generate_business_narrative,
)
from ppt_export import export_presentation


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI business recommendations from CSV data."
    )
    parser.add_argument(
        "csv_path",
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--output",
        default="Week 08/Day 3/output/business_recommendations.pptx",
        help="Output path for the PowerPoint presentation",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.is_file():
        parser.error(f"CSV file not found: {csv_path}")

    try:
        df = pd.read_csv(csv_path)

        if df.empty:
            raise ValueError("The CSV file contains no data rows.")

        insights = calculate_insights(df)

        print("\n=== FIVE DATA INSIGHTS ===")
        for number, insight in enumerate(insights, start=1):
            print(f"{number}. {insight}")

        print("\nGenerating executive summary and recommendations with Groq...")
        narrative = generate_business_narrative(insights)

        print("\n=== AI BUSINESS NARRATIVE ===\n")
        print(narrative)

        output = export_presentation(
            insights,
            narrative,
            args.output,
        )
        print(f"\nPowerPoint saved to: {output}")

    except (ValueError, RuntimeError, pd.errors.ParserError) as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
