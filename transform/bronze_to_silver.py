from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
BRONZE_BINANCE_DIR = BASE_DIR / 'data' / 'bronze' / 'binance'
BRONZE_FNG_DIR = BASE_DIR / 'data' / 'bronze' / 'fear_greed'
SILVER_DIR = BASE_DIR / 'data' / 'silver'
SILVER_DIR.mkdir(parents=True, exist_ok=True)

BINANCE_COLUMNS = [
    'open_time',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'close_time',
    'quote_asset_volume',
    'num_trades',
    'taker_buy_base',
    'taker_buy_quote',
    'ignore',
]


def _latest_json_file(folder: Path) -> Path:
    files = sorted(folder.glob('*.json'))
    if not files:
        raise FileNotFoundError(f'No JSON files found in {folder}')
    return files[-1]


def build_binance_silver() -> pd.DataFrame:
    latest_file = _latest_json_file(BRONZE_BINANCE_DIR)
    with latest_file.open('r', encoding='utf-8') as f:
        raw = json.load(f)

    df = pd.DataFrame(raw, columns=BINANCE_COLUMNS)
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['date'] = pd.to_datetime(df['open_time'], unit='ms').dt.date
    silver = df[[
        'date',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'quote_asset_volume',
        'num_trades',
    ]].rename(columns={
        'close': 'btc_close',
        'volume': 'btc_volume',
        'quote_asset_volume': 'btc_quote_volume',
        'num_trades': 'btc_num_trades',
    })

    silver = silver.sort_values('date').drop_duplicates(subset=['date'])
    silver.to_csv(SILVER_DIR / 'btc_daily_clean.csv', index=False)
    return silver


def build_fng_silver() -> pd.DataFrame:
    latest_file = _latest_json_file(BRONZE_FNG_DIR)
    with latest_file.open('r', encoding='utf-8') as f:
        raw = json.load(f)

    df = pd.DataFrame(raw['data'])
    df['date'] = pd.to_datetime(df['timestamp'].astype(int), unit='s').dt.date
    df['fear_greed_value'] = pd.to_numeric(df['value'], errors='coerce')
    silver = df[[
        'date',
        'fear_greed_value',
        'value_classification',
    ]].rename(columns={'value_classification': 'fear_greed_label'})

    silver = silver.sort_values('date').drop_duplicates(subset=['date'])
    silver.to_csv(SILVER_DIR / 'fear_greed_clean.csv', index=False)
    return silver


if __name__ == '__main__':
    btc = build_binance_silver()
    fng = build_fng_silver()
    print('Silver files created:')
    print(f'  - btc_daily_clean.csv ({len(btc)} rows)')
    print(f'  - fear_greed_clean.csv ({len(fng)} rows)')
