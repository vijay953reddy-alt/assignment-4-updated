from ingest_binance import fetch_binance_klines, save_snapshot as save_binance
from ingest_fear_greed import fetch_fear_greed, save_snapshot as save_fng


if __name__ == '__main__':
    binance_payload = fetch_binance_klines()
    fng_payload = fetch_fear_greed()

    binance_file = save_binance(binance_payload, symbol='BTCUSDT')
    fng_file = save_fng(fng_payload)

    print('Ingestion finished successfully.')
    print(f'  - {binance_file}')
    print(f'  - {fng_file}')
