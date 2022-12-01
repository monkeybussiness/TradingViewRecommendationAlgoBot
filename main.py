import asyncio
import time
import requests
from aiogram import Bot, Dispatcher, executor, types
from binance.client import Client
from tradingview_ta import TA_Handler, Interval
from config import TOKEN_API, SECRET_KEY

SYMBOL = 'ICXUSDT'
INTERVAL = Interval.INTERVAL_30_MINUTES
QNTY = 31


class Account:
    buy_flag = False
    sell_flag = False
    on_pos = False
    balance = 10
    open_pos_size = 0
    open_pos_price = 0
    close_pos_price = 0
    profit = 0
    pnl = 0


client = Client(api_key=TOKEN_API, api_secret=SECRET_KEY)
ac = Account()


def get_data():
    output = TA_Handler(symbol=SYMBOL,
                        screener='Crypto',
                        exchange='Binance',
                        interval=INTERVAL)
    activity = output.get_analysis().summary
    return activity


def place_order(order_type):
    if order_type == 'BUY':
        order = client.futures_create_order(symbol=SYMBOL, side=order_type, type='MARKET', quantity=QNTY)
        print(order)
    if order_type == 'SELL':
        order = client.futures_create_order(symbol=SYMBOL, side=order_type, type='MARKET', quantity=QNTY)
        print(order)


def main():
    print('Script are running...')
    while True:
        try:
            data = get_data()
            now_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
            if float(ac.open_pos_price) > 0 and ac.buy_flag is True:
                ac.pnl = -((ac.open_pos_price * ac.open_pos_size) - (ac.open_pos_size * now_price))
            elif float(ac.open_pos_price) > 0 and ac.sell_flag is True:
                ac.pnl = (ac.open_pos_price * ac.open_pos_size) - (ac.open_pos_size * now_price)
            else:
                ac.pnl = 0
            now_price = client.futures_ticker(symbol=SYMBOL)['lastPrice']

            # ОТКРЫТИЕ СДЕЛКИ
            if data['RECOMMENDATION'] == 'BUY' and ac.buy_flag is False and ac.on_pos is False:
                print('Открываю лонг')
                ac.buy_flag = True
                ac.on_pos = True
                ac.open_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.open_pos_size = ac.balance / ac.open_pos_price
                place_order("BUY")

            if data['RECOMMENDATION'] == 'SELL' and ac.sell_flag is False and ac.on_pos is False:
                print('Открываю Шорт')
                ac.sell_flag = True
                ac.on_pos = True
                ac.open_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.open_pos_size = ac.balance / ac.open_pos_price
                place_order("SELL")

            if data['RECOMMENDATION'] == 'STRONG BUY' and ac.buy_flag is False and ac.on_pos is False:
                print('Открываю Лонг')
                ac.buy_flag = True
                ac.on_pos = True
                ac.open_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.open_pos_size = ac.balance / ac.open_pos_price
                place_order("BUY")

            if data['RECOMMENDATION'] == 'STRONG SELL' and ac.sell_flag is False and ac.on_pos is False:
                print('Открываю Шорт')
                ac.sell_flag = True
                ac.on_pos = True
                ac.open_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.open_pos_size = ac.balance / ac.open_pos_price
                place_order("SELL")

            # ЗАКРЫТИЕ СДЕЛКИ
            if data['RECOMMENDATION'] == 'BUY' and ac.sell_flag is True and ac.on_pos is True:
                print('Закрываю Шорт')
                ac.sell_flag = False
                ac.buy_flag = False
                ac.on_pos = False
                ac.close_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.balance = ac.balance + ac.pnl
                place_order("BUY")

            if data['RECOMMENDATION'] == 'SELL' and ac.buy_flag is True and ac.on_pos is True:
                print('Закрываю Лонг')
                ac.sell_flag = False
                ac.buy_flag = False
                ac.on_pos = False
                ac.close_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.balance = ac.balance + ac.pnl
                place_order("SELL")

            if data['RECOMMENDATION'] == 'STRONG BUY' and ac.sell_flag is True and ac.on_pos is True:
                print('Закрываю Шорт')
                ac.buy_flag = True
                ac.on_pos = True
                ac.close_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.balance = ac.balance + ac.pnl
                place_order("BUY")

            if data['RECOMMENDATION'] == 'STRONG SELL' and ac.buy_flag is True and ac.on_pos is True:
                print('Закрываю Лонг')
                ac.sell_flag = False
                ac.buy_flag = False
                ac.on_pos = False
                ac.close_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.balance = ac.balance + ac.pnl
                place_order("SELL")

            else:
                print(data)
                print(f'Цена открытия сделки: {ac.open_pos_price}')
                print(f'Текущая цена: {now_price}')
                print(f'PNL: {ac.pnl}')
                print(f'Текущий баланс равен: {ac.balance + ac.pnl}')
            time.sleep(10)
        except requests.exceptions.ReadTimeout:
            print('requests.exceptions.ReadTimeout:')
            time.sleep(60)
            data = get_data()
            now_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
            if float(ac.open_pos_price) > 0 and ac.buy_flag is True:
                ac.pnl = -((ac.open_pos_price * ac.open_pos_size) - (ac.open_pos_size * now_price))
            elif float(ac.open_pos_price) > 0 and ac.sell_flag is True:
                ac.pnl = (ac.open_pos_price * ac.open_pos_size) - (ac.open_pos_size * now_price)
            else:
                ac.pnl = 0
            now_price = client.futures_ticker(symbol=SYMBOL)['lastPrice']

            # ОТКРЫТИЕ СДЕЛКИ
            if data['RECOMMENDATION'] == 'BUY' and ac.buy_flag is False and ac.on_pos is False:
                print('Открываю лонг')
                ac.buy_flag = True
                ac.on_pos = True
                ac.open_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.open_pos_size = ac.balance / ac.open_pos_price
                place_order("BUY")

            if data['RECOMMENDATION'] == 'SELL' and ac.sell_flag is False and ac.on_pos is False:
                print('Открываю Шорт')
                ac.sell_flag = True
                ac.on_pos = True
                ac.open_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.open_pos_size = ac.balance / ac.open_pos_price
                place_order("SELL")

            if data['RECOMMENDATION'] == 'STRONG BUY' and ac.buy_flag is False and ac.on_pos is False:
                print('Открываю Лонг')
                ac.buy_flag = True
                ac.on_pos = True
                ac.open_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.open_pos_size = ac.balance / ac.open_pos_price
                place_order("BUY")

            if data['RECOMMENDATION'] == 'STRONG SELL' and ac.sell_flag is False and ac.on_pos is False:
                print('Открываю Шорт')
                ac.sell_flag = True
                ac.on_pos = True
                ac.open_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.open_pos_size = ac.balance / ac.open_pos_price
                place_order("SELL")

            # ЗАКРЫТИЕ СДЕЛКИ
            if data['RECOMMENDATION'] == 'BUY' and ac.sell_flag is True and ac.on_pos is True:
                print('Закрываю Шорт')
                ac.sell_flag = False
                ac.buy_flag = False
                ac.on_pos = False
                ac.close_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.balance = ac.balance + ac.pnl
                place_order("BUY")

            if data['RECOMMENDATION'] == 'SELL' and ac.buy_flag is True and ac.on_pos is True:
                print('Закрываю Лонг')
                ac.sell_flag = False
                ac.buy_flag = False
                ac.on_pos = False
                ac.close_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.balance = ac.balance + ac.pnl
                place_order("SELL")

            if data['RECOMMENDATION'] == 'STRONG BUY' and ac.sell_flag is True and ac.on_pos is True:
                print('Закрываю Шорт')
                ac.buy_flag = True
                ac.on_pos = True
                ac.close_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.balance = ac.balance + ac.pnl
                place_order("BUY")

            if data['RECOMMENDATION'] == 'STRONG SELL' and ac.buy_flag is True and ac.on_pos is True:
                print('Закрываю Лонг')
                ac.sell_flag = False
                ac.buy_flag = False
                ac.on_pos = False
                ac.close_pos_price = float(client.futures_ticker(symbol=SYMBOL)['lastPrice'])
                ac.balance = ac.balance + ac.pnl
                place_order("SELL")

            else:
                print(data)
                print(f'Цена открытия сделки: {ac.open_pos_price}')
                print(f'Текущая цена: {now_price}')
                print(f'PNL: {ac.pnl}')
                print(f'Текущий баланс равен: {ac.balance + ac.pnl}')
            time.sleep(10)


if __name__ == '__main__':
    main()
