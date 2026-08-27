import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Number of customers
n = 5000

# Customer segments
segments = ['Premium', 'Business', 'Standard', 'Basic']
segment_weights = [0.15, 0.20, 0.35, 0.30]

# Payment methods
payment_methods = ['Credit Card', 'Debit Card', 'Bank Transfer', 'Mobile Money', 'Cash']
payment_weights = [0.30, 0.25, 0.20, 0.15, 0.10]

# Contract types
contract_types = ['Monthly', '1 Year', '2 Year']
contract_weights = [0.50, 0.30, 0.20]

# Support tiers
support_tiers = ['Basic', 'Standard', 'Premium']
support_weights = [0.40, 0.35, 0.25]

# Generate data
data = {
    'customer_id': range(1, n+1),
    'age': np.random.randint(18, 75, n),
    'gender': np.random.choice(['Male', 'Female'], n, p=[0.48, 0.52]),
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n),
    'segment': np.random.choice(segments, n, p=segment_weights),
    'contract_type': np.random.choice(contract_types, n, p=contract_weights),
    'tenure_months': np.random.exponential(24, n).astype(int).clip(1, 120),
    'monthly_charges': np.random.normal(65, 25, n).clip(20, 150).round(2),
    'total_charges': np.random.normal(1200, 800, n).clip(50, 5000).round(2),
    'payment_method': np.random.choice(payment_methods, n, p=payment_weights),
    'support_tier': np.random.choice(support_tiers, n, p=support_weights),
    'support_tickets': np.random.poisson(2, n).clip(0, 15),
    'avg_response_time_hours': np.random.exponential(8, n).clip(1, 48).round(1),
    'satisfaction_score': np.random.normal(3.8, 1.2, n).clip(1, 5).round(1),
    'churn_risk_score': np.random.beta(2, 5, n).round(2) * 100,
    'monthly_revenue': np.random.normal(1400, 600, n).clip(300, 4000).round(2),
    'lifetime_value': np.random.normal(1500, 900, n).clip(100, 6000).round(2),
    'last_interaction_date': [datetime.today() - timedelta(days=np.random.randint(0, 90)) for _ in range(n)]
}

df = pd.DataFrame(data)

# Add derived columns
df['churn_risk_category'] = pd.cut(
    df['churn_risk_score'],
    bins=[0, 30, 60, 100],
    labels=['Low', 'Medium', 'High']
)

df['support_effectiveness'] = df['support_tickets'].apply(
    lambda x: 'Excellent' if x <= 1 else 'Good' if x <= 3 else 'Needs Improvement'
)

# Save to CSV
df.to_csv('telecom_data.csv', index=False)
print("✅ telecom_data.csv created with 5,000 customer records!")
print(f"📊 Customers: {len(df):,}")
print(f"💰 Total Revenue: ${df['monthly_revenue'].sum():,.2f}")
print(f"📈 Average Churn Risk: {df['churn_risk_score'].mean():.1f}%")


