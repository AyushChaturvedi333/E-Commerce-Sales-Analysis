import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("data/ecommerce_sales.csv")

print("===== DATASET OVERVIEW =====")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== FIRST 5 RECORDS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

# Convert Order_Date to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Basic statistics
print("\n===== STATISTICAL SUMMARY =====")
print(df.describe())

# Category-wise sales
category_sales = df.groupby("Category")["Sales"].sum().sort_values(
    ascending=False
)

print("\n===== SALES BY CATEGORY =====")
print(category_sales)

# Region-wise sales
region_sales = df.groupby("Region")["Sales"].sum().sort_values(
    ascending=False
)

print("\n===== SALES BY REGION =====")
print(region_sales)

# Product-wise sales
product_sales = df.groupby("Product")["Sales"].sum().sort_values(
    ascending=False
)

print("\n===== TOP 10 PRODUCTS BY SALES =====")
print(product_sales.head(10))

# Monthly sales
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

monthly_sales = df.groupby("Month")["Sales"].sum()

print("\n===== MONTHLY SALES =====")
print(monthly_sales.head(12))

# -----------------------------
# VISUALIZATIONS
# -----------------------------

# 1. Sales by Category
plt.figure(figsize=(10, 6))
category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/sales_by_category.png")
plt.show()

# 2. Sales by Region
plt.figure(figsize=(8, 5))
region_sales.plot(kind="bar")
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("visualizations/sales_by_region.png")
plt.show()

# 3. Monthly Sales Trend
plt.figure(figsize=(12, 6))
monthly_sales.plot(kind="line")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/monthly_sales_trend.png")
plt.show()

# 4. Profit by Category
profit_category = df.groupby("Category")["Profit"].sum().sort_values(
    ascending=False
)

plt.figure(figsize=(10, 6))
profit_category.plot(kind="bar")
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/profit_by_category.png")
plt.show()

print("\n===== ANALYSIS COMPLETED SUCCESSFULLY =====")
print("Charts saved in the visualizations folder.")