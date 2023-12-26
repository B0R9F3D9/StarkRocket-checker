from requests import get
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from config import THREADS, HIDE_ADDRESS


def main(address: str) -> str:
    url = f'https://starkrocket.xyz/api/check_wallet?address={address.lower()}'
    params = {'address': address.lower()}
    try:
        r = get(url, params)
        data = r.json()['result']
        return {
            'address': address[:5] + '...' + address[-5:] if HIDE_ADDRESS else address,
            'bridge_volume': max(data['criteria']['bridge_volume']) if data['criteria']['bridge_volume'] else 0,
            'contracts': max(data['criteria']['contracts_variety']) if data['criteria']['contracts_variety'] else 0,
            'transaction_volume': max(data['criteria']['transaction_volume']) if data['criteria']['transaction_volume'] else 0,
            'transaction_count': max(data['criteria']['transactions_frequency']) if data['criteria']['transactions_frequency'] else 0,
            'months': max(data['criteria']['transactions_over_time']) if data['criteria']['transactions_over_time'] else 0,
            'eligible': '✅' if data['eligible'] else '❌',
            'points': data['points']}
    except:
        return {
            'address': address[:5] + '...' + address[-5:] if HIDE_ADDRESS else address,
            'bridge_volume': 'ERROR',
            'contracts': 'ERROR',
            'transaction_volume': 'ERROR',
            'transaction_count': 'ERROR',
            'months': 'ERROR',
            'eligible': 'ERROR',
            'points': 'ERROR'}


if __name__ == '__main__':
    # Чтение адресов
    with open('addresses.txt', 'r', encoding='utf-8') as file:
        ADDRESSES = [x.strip() for x in file.readlines()]

    # Параллельное выполнение запросов
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        result = list(executor.map(main, ADDRESSES))

    # Вывод результатов
    print(tabulate(result, headers='keys', tablefmt='pretty'))

    # Запись результатов в файл
    df = pd.DataFrame(result)
    df.to_excel('result.xlsx', index=False)
    print('The results are saved in the file result.xlsx')
