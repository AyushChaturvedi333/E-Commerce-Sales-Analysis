import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Number of records
n = 5000

# Product information
products = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Smartwatch", "Tablet"],
    "Furniture": ["Office Chair", "Desk", "Bookshelf", "Sofa", "Table"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes", "Dress"],
    "Home & Kitchen": ["Mixer", "Cookware Set", "Air Fryer", "Coffee Maker", "Dinner Set"],
    "Books": ["Programming Book", "Novel", "Data Science Book", "Business Book", "Exam Guide"]
}

regions = ["North", "South", "East", "West"]
cities = ["Delhi", "Mumbai", "Bengaluru", "Jaipur", "Kolkata",
          "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Lucknow"]

payment_modes = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking"]
customer_segments = ["Consumer", "Corporate", "Home Office"]

categories = np.random.choice(list(products.keys()), n)

product_names = []
for category in categories:
    product_names.append(np.random.choice(products[category]))

data = pd.DataFrame({
    "Order_ID": [f"ORD{100001 + i}" for i in range(n)],
    "Order_Date": pd.date_range(
        start="2024-01-01",
        end="2025-12-31",
        periods=n
    ),
    "Product": product_names,
    "Category": categories,
    "Region": np.random.choice(regions, n),
    "City": np.random.choice(cities, n),
    "Sales": np.round(np.random.uniform(200, 50000, n), 2),
    "Quantity": np.random.randint(1, 10, n),
    "Discount": np.round(np.random.uniform(0, 0.40, n), 2),
    "Payment_Mode": np.random.choice(payment_modes, n),
    "Customer_Segment": np.random.choice(customer_segments, n)
})

# Calculate profit
data["Profit"] = np.round(
    data["Sales"] * np.random.uniform(0.05, 0.30, n)
    * (1 - data["Discount"]),
    2
)

# Sort by date
data = data.sort_values("Order_Date").reset_index(drop=True)

# Save dataset
data.to_csv("data/ecommerce_sales.csv", index=False)

print("Dataset created successfully!")
print(f"Total records: {len(data)}")
print("File saved to: data/ecommerce_sales.csv")
print("\nFirst 5 records:")
print(data.head())