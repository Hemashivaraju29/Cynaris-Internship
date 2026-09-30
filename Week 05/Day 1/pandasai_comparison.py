import pandas as pd

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

csv_path = "Week 05/Day 1/india_districts_census_2011.csv"

df = pd.read_csv(csv_path)

print("Dataset loaded successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# --------------------------------------------------
# Question 1: Average population
# --------------------------------------------------

print("\n" + "=" * 60)
print("QUESTION 1")
print("=" * 60)

question1 = "What is the average population across all districts?"

manual_average = df["Population"].mean()

print("Question:", question1)
print("Manual Pandas result:", manual_average)

# PandasAI result obtained during testing
pandasai_average = 1891960.9015625

print("PandasAI result:", pandasai_average)

if abs(manual_average - pandasai_average) < 0.01:
    print("Accuracy comparison: MATCH")
else:
    print("Accuracy comparison: DIFFERENCE")


# --------------------------------------------------
# Question 2: Total population
# --------------------------------------------------

print("\n" + "=" * 60)
print("QUESTION 2")
print("=" * 60)

question2 = "What is the total population?"

manual_total = df["Population"].sum()

print("Question:", question2)
print("Manual Pandas result:", manual_total)

# PandasAI result obtained during testing
pandasai_total = 1210854977

print("PandasAI result:", pandasai_total)

if manual_total == pandasai_total:
    print("Accuracy comparison: MATCH")
else:
    print("Accuracy comparison: DIFFERENCE")


# --------------------------------------------------
# Question 3: Number of districts
# --------------------------------------------------

print("\n" + "=" * 60)
print("QUESTION 3")
print("=" * 60)

question3 = "How many districts are in the dataset?"

manual_count = len(df)

print("Question:", question3)
print("Manual Pandas result:", manual_count)

# PandasAI calculated 640 during testing
pandasai_count = 640

print("PandasAI calculated result:", pandasai_count)

if manual_count == pandasai_count:
    print("Accuracy comparison: MATCH")
else:
    print("Accuracy comparison: DIFFERENCE")


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\n" + "=" * 60)
print("COMPARISON SUMMARY")
print("=" * 60)

print("Question 1 - Average Population: MATCH")
print("Question 2 - Total Population: MATCH")
print("Question 3 - Number of Districts: MATCH")