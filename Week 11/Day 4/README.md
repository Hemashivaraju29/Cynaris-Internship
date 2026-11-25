# W11D4 - Metabase Self-Serve BI Setup

## Objective
Set up Metabase as a self-service Business Intelligence (BI) tool, connect it to a PostgreSQL database, create sales visualizations, and build an executive dashboard.

## Tools and Technologies
- Metabase
- Docker Desktop
- PostgreSQL
- Docker
- PowerShell
- Git and GitHub

## Setup and Database Connection
1. Started Docker Desktop.
2. Ran Metabase in a Docker container on port 3000.
3. Connected the Metabase container to the existing PostgreSQL Docker network.
4. Added the PostgreSQL database to Metabase.
5. Configured the database connection using the PostgreSQL host, port, database name, username, and password.
6. Verified the connection and accessed the `Cynaris Sales` table.

## Dashboard Visualizations

Created and saved the following five questions in Metabase:

1. **Sales by Region** - Bar chart showing total sales for each region.
2. **Monthly Sales Trend** - Line chart showing monthly sales performance.
3. **Sales by Category** - Pie chart showing the contribution of each product category.
4. **Sales Transactions Table** - Table displaying date, region, category, sales, and units sold.
5. **Total Sales** - Number visualization displaying the overall sales amount.

## Key Findings

- Total sales: Rs. 308,400
- Average transaction value: Rs. 12,850
- Total units sold: 1,079
- Highest sales region: South (Rs. 89,200)
- Highest sales category: Electronics (Rs. 133,000)

## Executive Dashboard

Created a dashboard named **Cynaris Sales Executive Dashboard** and added all five visualizations.

The dashboard provides an overview of sales performance, regional contribution, category distribution, monthly trends, and individual transactions.

## Dashboard Screenshot

Screenshot location:

`outputs/Cynaris_Sales_Executive_Dashboard.png`

## Stakeholder Sharing

- Share the dashboard with authorized stakeholders through Metabase's sharing options, subject to user permissions and access configuration.
- Ensure database and collection permissions are configured before sharing.
- Avoid exposing sensitive database credentials or making business data publicly accessible.
- Stakeholders can use the dashboard to explore sales performance and support data-driven decisions.

## Outcome

Successfully configured Metabase using Docker, connected it to PostgreSQL, created five sales visualizations, and built an executive dashboard for self-service business intelligence.
