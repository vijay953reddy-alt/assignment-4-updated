from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
SILVER_DIR = BASE_DIR / 'data' / 'silver'
GOLD_DIR = BASE_DIR / 'data' / 'gold'
GOLD_DIR.mkdir(parents=True, exist_ok=True)


def build_gold() -> pd.DataFrame:
    btc = pd.read_csv(SILVER_DIR / 'btc_daily_clean.csv', parse_dates=['date'])
    fng = pd.read_csv(SILVER_DIR / 'fear_greed_clean.csv', parse_dates=['date'])

    gold = btc.merge(fng, on='date', how='inner')
    gold = gold.sort_values('date').reset_index(drop=True)

    gold['btc_daily_return'] = gold['btc_close'].pct_change()
    gold['positive_return'] = (gold['btc_daily_return'] > 0).astype('Int64')
    gold['is_weekend'] = (gold['date'].dt.dayofweek >= 5).astype(int)
    gold['sentiment_group'] = gold['fear_greed_label'].replace({
        'Extreme Fear': 'Fear',
        'Fear': 'Fear',
        'Neutral': 'Neutral',
        'Greed': 'Greed',
        'Extreme Greed': 'Greed',
    })
    gold['high_sentiment_day'] = gold['fear_greed_value'].ge(55).astype(int)

    gold = gold.dropna(subset=['btc_daily_return']).copy()
    gold['date'] = gold['date'].dt.date
    gold.to_csv(GOLD_DIR / 'crypto_sentiment_daily.csv', index=False)
    return gold


if __name__ == '__main__':
    gold = build_gold()
    print(f'Gold file created: crypto_sentiment_daily.csv ({len(gold)} rows)')
