import os
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv("Amazon.csv")

print("\nFirst 5 Records")
print(df.head())

print("\nDataset Information")
df.info()

print("\nMissing Values")
print(df.isnull().sum())

# Data Cleaning
df.drop_duplicates(inplace=True)

df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

# Remove rows with invalid dates
df.dropna(subset=["OrderDate"], inplace=True)

# Create Sales and Profit Columns
df["Sales"] = df["TotalAmount"]
df["Profit"] = df["Sales"] * 0.20      # Estimated Profit (20%)


# KPI Analysis
print("\n========== KPI ==========")

print("Total Sales      :", round(df["Sales"].sum(), 2))
print("Total Profit     :", round(df["Profit"].sum(), 2))
print("Total Orders     :", df["OrderID"].nunique())
print("Average Sales    :", round(df["Sales"].mean(), 2))
print("Average Profit   :", round(df["Profit"].mean(), 2))
print("Maximum Sales    :", round(df["Sales"].max(), 2))
print("Minimum Sales    :", round(df["Sales"].min(), 2))

# Sales by State
state = df.groupby("State")["Sales"].sum().sort_values(ascending=False)

print("\nSales by State")
print(state)


# Sales by Category
category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

print("\nSales by Category")
print(category)

# Top 10 Products
top = (
    df.groupby("ProductName")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products")
print(top)

# Top 5 Customers
customer = (
    df.groupby("CustomerName")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTop 5 Customers")
print(customer)

# Payment Method
payment = df["PaymentMethod"].value_counts()

print("\nPayment Methods")
print(payment)

# Monthly Sales Trend
df["Month"] = df["OrderDate"].dt.month_name()

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly = (
    df.groupby("Month")["Sales"]
    .sum()
    .reindex(month_order)
)

print("\nMonthly Sales")
print(monthly)

# Create Charts Folder
os.makedirs("charts", exist_ok=True)

# Sales by State
plt.figure(figsize=(10,6))

state.plot(kind="bar")

plt.title("Sales by State")
plt.xlabel("State")
plt.ylabel("Sales")
plt.tight_layout()

plt.savefig("charts/state_sales.png")

plt.show()

# Sales by Category
plt.figure(figsize=(7,7))

category.plot(kind="pie", autopct="%1.1f%%")

plt.title("Category-wise Sales")
plt.ylabel("")

plt.tight_layout()

plt.savefig("charts/category_sales.png")

plt.show()

# Monthly Sales Trend
plt.figure(figsize=(10,6))

monthly.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("charts/monthly_sales.png")

plt.show()

# Top 10 Products
plt.figure(figsize=(10,6))

top.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("charts/top_products.png")

plt.show()

print("\nAnalysis Completed Successfully!")
print("Charts saved inside the 'charts' folder.")
