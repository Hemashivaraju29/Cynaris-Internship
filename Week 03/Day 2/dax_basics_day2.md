# Week 3 Day 2 - DAX Basics

## 1. CALCULATE()

CALCULATE() changes the filter context of a calculation.

Example:

Online Sales =
CALCULATE(
[Total Sales],
da_sales_transactions[Channel] = "Website"
)

This calculates Total Sales only for the Website channel.

## 2. YTD Sales

DATESYTD() calculates values from the beginning of the year up to the current date.

Example:

YTD Sales =
CALCULATE(
[Total Sales],
DATESYTD(da_sales_transactions[Date])
)

## 3. Running Total using EARLIER()

EARLIER() allows a calculated column to access the value from the current row while another row context is being evaluated.

The Running Total column compares each Transaction_ID with earlier Transaction_ID values and calculates cumulative sales.

## 4. Profit Margin % (Proxy)

The dataset does not contain a cost column, so a true profit margin cannot be calculated.

A proxy was created using the available discount percentage:

Profit Margin % (Proxy) = 100 - Discount_Pct

This should not be interpreted as an accounting profit margin.

## 5. Row Context

Row context means DAX evaluates one row at a time. It is commonly used in calculated columns.

## 6. Filter Context

Filter context is the set of filters applied when a measure is evaluated.

For example, CALCULATE() can modify the filter context to calculate Website sales only.

## 7. Context Transition

Context transition occurs when CALCULATE() converts the current row context into an equivalent filter context.

In simple terms:

Row Context
↓
CALCULATE()
↓
Filter Context

This allows DAX to evaluate calculations using the current row as a filter.
