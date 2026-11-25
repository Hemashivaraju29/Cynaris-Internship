import argparse
import pandas as pd
from executive_summary import calculate_insights, generate_summary
from ppt_export import export_presentation


def main():
    parser = argparse.ArgumentParser(
        description="CSV to Groq executive summary and PowerPoint"
    )
    parser.add_argument("csv_path", help="Path to the input CSV file")
    parser.add_argument(
        "--output",
        default="Week 08/Day 1/output/executive_summary.pptx",
        help="Path for the generated PowerPoint",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.csv_path)
    insights = calculate_insights(df)

    print("\n=== FIVE DATA INSIGHTS ===")
    for number, insight in enumerate(insights, start=1):
        print(f"{number}. {insight}")

    summary = generate_summary(insights)
    print("\n=== GROQ EXECUTIVE SUMMARY ===\n")
    print(summary)

    output = export_presentation(insights, summary, args.output)
    print(f"\nPowerPoint saved to: {output}")


if __name__ == "__main__":
    main()
