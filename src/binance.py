import ccxt
import pandas

import config


class BinanceData:
    def __init__(self):
        self.binance = ccxt.binance(config={
            'apiKey': config.BINANCE_API_KEY,
            'secret': config.BINANCE_API_SECRET_KEY
        })

    def test(self):
        btc = self.binance.fetch_ticker('BTC/USDT')

        # etch_ohlcv 메소드를 사용하면 특정 암호화폐의 분봉 데이터를 500개까지 얻을 수 있습니다
        btc_ohlcv = self.binance.fetch_ohlcv('BTC/USDT')
        df = pandas.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pandas.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)
        # print(df)

        # 일봉 조회 역시 fetch_ohlcv 메소드를 사용하여 조회합니다. (메소드의 인자로 추가로 '1d'를 전달)
        btc_ohlcv_d = self.binance.fetch_ohlcv('BTC/USDT', '1d')
        df = pandas.DataFrame(btc_ohlcv_d, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pandas.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)
        # print(df)

        btc_ohlcv_pagination = self.binance.fetch_ohlcv(symbol='BTC/USDT', timeframe='1d', limit=10)
        df = pandas.DataFrame(btc_ohlcv_pagination, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pandas.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)
        # print(df)

        # 호가 조회
        exchange = ccxt.binance()
        orderbook = exchange.fetch_order_book('ETH/USDT')
        # print(orderbook['asks'])
        # print(orderbook['bids'])

    def get_account_price(self):
        balance = self.binance.fetch_balance()
        # free => 거래에 사용하고 있지 않은 코인양
        # used => 거래에 사용하고 있는 코인양
        # total = free + used
        print(balance['USDT'])
        return balance['USDT']

    def set_order(self):
        # amount => 갯수
        # price => 지정가
        # !! 일단 실행 시키지 말 것
        # 시장가 주문은 create_market_sell_order 메서드 사용
        order = self.binance.create_limit_buy_order(symbol='BTC/USDT', amount=0.01, price=20000)

    def cancel_order(self):
        # id => order 하고 받은 id 값
        res = self.binance.cancel_order(id='5555', symbol='BTC/USDT')


'''
    ask => 매도 1호가 (가장 싸게 팔려고 내놓은 가격)
    askVolume => 매도 1호과 물량
    bid => 매수 1호가 (가장 비싸게 사려고 내놓은 가격)
    bidVolume => 매수 1호과 물량
    datetime => 현재 시간
    timestamp => 타임 스탬프
    open => 시가
    high => 고가 
    low => 저가
    close => 종가
    symbol => 심
'''
