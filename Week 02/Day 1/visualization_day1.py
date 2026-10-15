# Data Visualization - Week 2 Day 1

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned sales data
df = pd.read_csv("Week 01/Day 5/sales_cleaned.csv")

# Apply Seaborn theme
sns.set_theme(style="whitegrid")

print("Sales Data:")
print(df)

# --------------------------------------------------
# 1. LINE CHART - Sales Amount by Sale ID
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["sale_id"],
    df["amount"],
    marker="o",
    linewidth=2
)

plt.title("Sales Amount by Sale ID")
plt.xlabel("Sale ID")
plt.ylabel("Sales Amount")

# Data callouts
for x, y in zip(df["sale_id"], df["amount"]):
    plt.annotate(
        f"₹{y:,.0f}",
        (x, y),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center"
    )

plt.tight_layout()
plt.savefig(
    "Week 02/Day 1/line_chart.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# --------------------------------------------------
# 2. BAR CHART - Sales by Category
# --------------------------------------------------

category_sales = df.groupby(
    "category",
    as_index=False
)["amount"].sum()

plt.figure(figsize=(8, 5))

ax = sns.barplot(
    data=category_sales,
    x="category",
    y="amount"
)

plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")

# Data callouts
for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"₹{value:,.0f}" for value in container.datavalues]
    )

plt.tight_layout()
plt.savefig(
    "Week 02/Day 1/bar_chart.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# --------------------------------------------------
# 3. SCATTER PLOT - Quantity vs Sales Amount
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="quantity",
    y="amount",
    hue="category",
    s=120
)

plt.title("Quantity vs Sales Amount")
plt.xlabel("Quantity")
plt.ylabel("Sales Amount")

plt.tight_layout()
plt.savefig(
    "Week 02/Day 1/scatter_chart.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# --------------------------------------------------
# 4. HISTOGRAM - Distribution of Sales Amount
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="amount",
    bins=5,
    kde=True
)

plt.title("Distribution of Sales Amount")
plt.xlabel("Sales Amount")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig(
    "Week 02/Day 1/histogram.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# --------------------------------------------------
# 5. BOX PLOT - Sales Amount by Category
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="category",
    y="amount"
)

plt.title("Sales Amount by Category")
plt.xlabel("Category")
plt.ylabel("Sales Amount")

plt.tight_layout()
plt.savefig(
    "Week 02/Day 1/box_plot.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


print("\nAll charts created and saved successfully!")