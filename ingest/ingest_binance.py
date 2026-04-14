from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
BRONZE_DIR = BASE_DIR / 'data' / 'bronze' / 'binance'
BRONZE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_binance_klines(symbol: str = 'BTCUSDT', interval: str = '1d', limit: int = 365) -> list:
    url = 'https://api.binance.com/api/v3/klines'

    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_snapshot(payload: list, symbol: str) -> Path:
    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    output_path = BRONZE_DIR / f'{symbol.lower()}_klines_{timestamp}.json'
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return output_path


if __name__ == '__main__':
    symbol = os.getenv('CRYPTO_SYMBOL', 'BTCUSDT')
    interval = os.getenv('BINANCE_INTERVAL', '1d')
    lookback_days = int(os.getenv('LOOKBACK_DAYS', '365'))

    payload = fetch_binance_klines(symbol=symbol, interval=interval, limit=lookback_days)
    output_file = save_snapshot(payload, symbol=symbol)
    print(f'Saved Binance snapshot to: {output_file}')
