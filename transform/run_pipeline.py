from bronze_to_silver import build_binance_silver, build_fng_silver
from silver_to_gold import build_gold


if __name__ == '__main__':
    build_binance_silver()
    build_fng_silver()
    gold = build_gold()
    print('Pipeline complete.')
    print(f'Gold rows: {len(gold)}')
