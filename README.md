# Assignment 3 — Data Pipeline for Statistical Analysis

## Recommended choice: Pack A (Crypto & Sentiment)

I picked **Pack A** because it is the simplest pack to finish cleanly and it already supports all the statistics you may need in Part 2:
- one-sample t-test on daily BTC returns,
- two-sample t-test on returns across sentiment groups,
- proportion z-test on positive-return days.

This repo follows the required **Bronze → Silver → Gold** medallion structure.

---

## Project question

**Does Bitcoin behave differently on Fear vs Greed days?**

That question is a good fit because:
- Binance gives daily market data like close price and volume.
- Alternative.me gives daily sentiment values and labels.
- Both sources can be joined by **date**.

---

## APIs used

### 1) Binance Spot API
Used for daily BTC/USDT OHLCV candles.

Endpoint used:
```python
https://api.binance.com/api/v3/klines
```

Parameters used:
- `symbol=BTCUSDT`
- `interval=1d`
- `limit=365`

### 2) Alternative.me Fear & Greed Index API
Used for daily crypto sentiment values and labels.

Endpoint used:
```python
https://api.alternative.me/fng/
```

Parameters used:
- `limit=365`
- `format=json`

---

## Folder structure

```text
assignment3_solution/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── analysis_preview.md
├── data/
│   ├── bronze/
│   │   ├── binance/
│   │   └── fear_greed/
│   ├── silver/
│   └── gold/
├── ingest/
│   ├── ingest_binance.py
│   ├── ingest_fear_greed.py
│   └── run_ingestion.py
├── transform/
│   ├── bronze_to_silver.py
│   ├── silver_to_gold.py
│   └── run_pipeline.py
└── notebooks/
    └── assignment3_starter.ipynb
```

---

## What each layer contains

### Bronze
Raw API snapshots saved exactly as returned.

Examples:
- `data/bronze/binance/btc_klines_2026-04-01T00-00-00.json`
- `data/bronze/fear_greed/fng_2026-04-01T00-00-00.json`

### Silver
Cleaned one-table-per-source files.

Files:
- `data/silver/btc_daily_clean.csv`
- `data/silver/fear_greed_clean.csv`

### Gold
Final analysis-ready joined table.

File:
- `data/gold/crypto_sentiment_daily.csv`

---

## Derived columns created in Gold

The Gold dataset includes:
- `btc_close`
- `btc_volume`
- `btc_daily_return`
- `fear_greed_value`
- `fear_greed_label`
- `positive_return`
- `is_weekend`
- `sentiment_group`
- `high_sentiment_day`

### Why these columns matter
- `btc_daily_return` gives a continuous metric for t-tests.
- `positive_return` gives a binary outcome for a proportion z-test.
- `sentiment_group` gives a grouping variable for comparison.

---

## How to run

### 1) Create environment and install packages

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 2) Run ingestion

```bash
python ingest/ingest_binance.py
python ingest/ingest_fear_greed.py
```

Or run both:

```bash
python ingest/run_ingestion.py
```

### 3) Transform Bronze to Silver and Gold

```bash
python transform/bronze_to_silver.py
python transform/silver_to_gold.py
```

Or run the whole transform flow:

```bash
python transform/run_pipeline.py
```

---

## Cleaning decisions

### Binance
- Converted timestamp from milliseconds to `date`
- Converted numeric columns from strings to floats
- Kept only the columns needed for analysis
- Renamed columns to business-friendly names like `btc_close` and `btc_volume`

### Fear & Greed
- Converted unix timestamp to `date`
- Converted `value` to integer/numeric
- Renamed `value_classification` to `fear_greed_label`
- Kept one row per date

### Join strategy
- Used an **inner join on date**
- This ensures Gold only contains dates available in both sources
- This is the safest choice for Part 2 because each row must have both market data and sentiment data

---

## Suggested demo talking points

In your video, you can say:
1. Why you chose Pack A
2. What the raw Bronze JSON looks like
3. How you cleaned Binance and Fear & Greed separately in Silver
4. How you joined them on date
5. Why `btc_daily_return` and `positive_return` were created
6. What hypothesis you plan to test in Part 2
7. One challenge: matching dates and making sure data types were converted correctly

---

## AI Usage

AI tool used:
- ChatGPT

What it helped with:
- project structure,
- starter ingestion scripts,
- transformation logic,
- README and planning memo wording.

One thing I still had to verify myself:
- I had to confirm that both sources could be joined correctly on **daily dates** and that the return calculation used the previous day's close rather than the same row.
