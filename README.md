# Crypto & Sentiment Analysis Project (Assignment 3 + 4)

## Overview
This project analyzes the relationship between **Bitcoin returns** and **market sentiment (Fear & Greed Index)** using a full data pipeline and a Streamlit app.

---

# 📦 Assignment 3 — Data Pipeline

## Project Question
**Does Bitcoin behave differently on Fear vs Greed days?**

## APIs Used
- Binance API → BTC daily price & volume
- Alternative.me API → Fear & Greed Index

## Data Architecture (Medallion)
- **Bronze** → Raw JSON API data
- **Silver** → Cleaned datasets
- **Gold** → Joined analysis-ready dataset

## Gold Dataset Columns
- btc_close
- btc_volume
- btc_daily_return
- fear_greed_value
- fear_greed_label
- positive_return
- is_weekend
- sentiment_group
- high_sentiment_day

---

# 🚀 Assignment 4 — Streamlit Statistical App

## What I Added
I extended Assignment 3 by building an **interactive Streamlit dashboard** to perform statistical analysis.

## Features
- 📊 Data preview
- 📦 Boxplot: BTC returns (Working vs Non-working days)
- 🧪 Hypothesis testing:
  - One-sample t-test
  - Two-sample t-test
  - Chi-square test
  - Variance comparison (F-test)
  - Correlation analysis

## New Columns Used
- `non_working_day_flag`
- `is_weekend`
- `positive_return`

## App File