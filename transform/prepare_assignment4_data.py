import pandas as pd

# Load datasets
df = pd.read_csv("data/gold/crypto_sentiment_daily.csv")
holiday = pd.read_csv("data/gold/holiday_data.csv")

# Format dates
df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
holiday["date"] = pd.to_datetime(holiday["date"]).dt.strftime("%Y-%m-%d")

# Merge
df = df.merge(holiday, on="date", how="left")

# Fill missing holiday values
df["holiday_flag"] = df["holiday_flag"].fillna(0).astype(int)

# Create new column
df["positive_return"] = (df["btc_daily_return"] > 0).astype(int)

# Save final dataset
df.to_csv("data/gold/crypto_sentiment_daily_extended.csv", index=False)

print("Final dataset created!")