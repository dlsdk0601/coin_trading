from dataclasses import asdict
from enum import auto
from typing import Tuple

import pandas
from pandas import Series

from was.ex.calculate_trade_unit import calculate_trade_unit
from was.ex.date_ex import now
from was.ex.enum_ex import StringEnum
from was.ex.logger import log, LogLevel
from was.model.coin import MarketType
from was.repository import upbit
from was.repository.upbit import GetCandleDayReq, GetCandleDayResItem, GetTickerReq, order_buy_market, \
    OrderBuyMarketReq, order_sell_market, OrderSellMarketReq, Err


def upbit_current(req: MarketType):
    res = upbit.get_account()
    krw_account: upbit.GetAccountResItem | None = None
    match res:
        case upbit.Err(name=name, message=message):
            log.log(level=LogLevel.ERROR, text=f'UPBIT | DEPOSIT SELECT | ERROR | market={req.label} {name=} {message=}')
            return None
        case upbit.GetAccountRes(accounts=accounts):
            acc: upbit.GetAccountResItem
            for acc in accounts:
                if acc.currency == req.currency:
                    krw_account = acc

    return krw_account


def upbit_current_ticker(req: MarketType):
    res = upbit.get_ticker(GetTickerReq(markets=[req]))

    ticker: upbit.GetTickerResItem | None = None
    match res:
        case upbit.Err(name=name, message=message):
            log.log(level=LogLevel.ERROR,
                    text=f'UPBIT | TICKER SELECT | ERROR | market={req.label} {name=} {message=}')
            log.log(level=LogLevel.ERROR, text=f'error :: {name=} {message=}')
            return None
        case upbit.GetTickerRes(tickers=tickers):
            t: upbit.GetTickerResItem
            for t in tickers:
                if t.market == req.label:
                    ticker = t

    return ticker


def get_ohlcv(market: MarketType):
    res = upbit.get_candle_day(GetCandleDayReq(market=market, to=now().isoformat(), count=200))

    candles: list[GetCandleDayResItem] = []
    match res:
        case upbit.Err(name=name, message=message):
            log.log(level=LogLevel.ERROR, text=f'UPBIT | CANDLE SELECT | ERROR | market={market.label} {name=} {message=}')
            return None
        case upbit.GetCandleDayRes(candles=candles):
            candles = candles

    df = pandas.DataFrame([asdict(item) for item in candles])
    df['candle_date_time_kst'] = pandas.to_datetime(df['candle_date_time_kst'])
    df.set_index('candle_date_time_kst', inplace=True)
    df = df[['opening_price', 'high_price', 'low_price', 'trade_price', 'candle_acc_trade_volume']]
    df.rename(columns={
        'opening_price': 'open',
        'high_price': 'high',
        'low_price': 'low',
        'trade_price': 'close',
        'candle_acc_trade_volume': 'volume'
    }, inplace=True)

    return df


def get_bollinger_bands(prices: Series, window: int = 20, multiplier: int = 2) -> Tuple[Series, Series]:
    # 20 일 동안 이동 평균선 계산 (middle Band)
    sma = prices.rolling(window=window).mean()

    # 20 일 동안 표준편차 계싼
    rolling_std = prices.rolling(window=window).std()

    # 중간 밴드 => 이동 평균선 + (표준 편차 * 2)
    upper_band = sma + (rolling_std * multiplier)

    # 중간 밴드 => 이동 평균선 - (표준 편차 * 2)
    lower_band = sma - (rolling_std * multiplier)

    return upper_band, lower_band


class BollingerBandsSignal(StringEnum):
    HOLD = auto()
    SELL = auto()
    BUY = auto()


def bollinger_signal(market: MarketType, prices: Series) -> BollingerBandsSignal:
    upper_band, lower_band = get_bollinger_bands(prices=prices)

    band_high = upper_band.iloc[-1]
    band_low = lower_band.iloc[-1]
    current_ticker = upbit_current_ticker(req=market)
    current_price = current_ticker.trade_price

    '''
        현재 가겨이 상단 밴드보다 큰 경우 'BUY 신호
        하단 밴드보다 낮은 경우는 'SELL' 신호
        밴드안에 있는 경우는 'HOLD' 신호 
    '''
    res = BollingerBandsSignal.HOLD

    if current_price > band_high:
        res = BollingerBandsSignal.SELL
    if current_price < band_low:
        res = BollingerBandsSignal.BUY

    return BollingerBandsSignal.HOLD


def bollinger_trading(market: MarketType):
    log.log(level=LogLevel.INFO, text=f'BOLLINGER BAND START')
    # 분석할 데이터
    price_data = get_ohlcv(market=market)
    prices = price_data['close']

    # 판단
    signal = bollinger_signal(market=market, prices=prices)
    log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | SIGNAL {signal=}')

    # 현재 잔고
    account_krw = upbit_current(req=MarketType.KRW)
    balance_cash = float(account_krw.balance)
    log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | CASH ACCOUNT {balance_cash=}')

    # 잔고 코인
    account_coin = upbit_current(req=market)
    balance_coin = float(account_coin.balance)
    log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | COIN market={market.label} {balance_coin=}')

    # 현재 잔액에 10% 만 배팅
    buy_unit = calculate_trade_unit(balance_cash)
    log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | BETTING AMOUNT {buy_unit=}')

    if balance_cash < 10_000:
        # 잔액 부족
        log.log(level=LogLevel.WARNING, text=f'UPBIT | BOLLINGER BAND | LACK OF BALANCE {balance_cash=}')
        return None

    res = None
    match signal:
        case BollingerBandsSignal.BUY:
            if balance_cash > buy_unit:
                res = order_buy_market(OrderBuyMarketReq(market=market, price=balance_cash))
                log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | BUY SUCCESS {market.label} {balance_cash}', slack_send=True)
        case BollingerBandsSignal.SELL:
            if balance_coin > 0:
                res = order_sell_market(OrderSellMarketReq(market=market, volume=balance_coin))
                log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | SELL SUCCESS {market.label} {balance_coin}', slack_send=True)
        case BollingerBandsSignal.HOLD:
            # HOLD 는 아무것도 하지 않는다.
            log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | HOLD {market.label}')


    if isinstance(res, Err):
        log.log('TR', f'UPBIT | BOLLINGER BAND | BUY OR SELL | ERROR {signal=} message={res.message} name={res.name}', slack_send=True)
        return None

    return res