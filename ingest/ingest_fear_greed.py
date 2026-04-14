from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
BRONZE_DIR = BASE_DIR / 'data' / 'bronze' / 'fear_greed'
BRONZE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_fear_greed(limit: int = 365) -> dict:
    url = 'https://api.alternative.me/fng/'
    params = {'limit': limit, 'format': 'json'}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_snapshot(payload: dict) -> Path:
    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    output_path = BRONZE_DIR / f'fng_{timestamp}.json'
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return output_path


if __name__ == '__main__':
    lookback_days = int(os.getenv('LOOKBACK_DAYS', '365'))
    payload = fetch_fear_greed(limit=lookback_days)
    output_file = save_snapshot(payload)
    print(f'Saved Fear & Greed snapshot to: {output_file}')
