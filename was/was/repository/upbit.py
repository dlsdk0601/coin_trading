import pyupbit
from pyupbit import Upbit

from was import config
from was.ex.calculate_trade_unit import calculate_trade_unit
from was.ex.logger import log
from was.model.coin import CoinType


class UpbitData:
    def __init__(self):
        self.upbit = Upbit(config.UPBIT_ACCESS_KEY, config.UPBIT_SECRET_KEY)

    # 현재 보유 금액 조회
    def get_balance_cash(self) -> float | None:
        return self.upbit.get_balance('KRW')

    @staticmethod
    def get_current_price(ticker: CoinType | list[CoinType]) -> float:
        """현재가격 조회
        :param ticker: (CoinType | list[CoinType]) 단일 티커 또는 티커 리스트
        :return
            float : 현재 가격 (원화)
        """

        # str 타입으로 넘겨야해서 처리한다
        # upbit 에서 default 처리 해줘도 프로젝트 내에서는 필수값으로 한다.
        match ticker:
            case list():
                tickers = list(map(lambda coin: coin.label, ticker))
                return pyupbit.get_current_price(tickers)
            case  _:
                return pyupbit.get_current_price(ticker.label)


    def get_balance_coin(self, ticker: CoinType) -> float:
        """현재 본인이 보유하고 있는 해당 코인 수량 조회
        :param ticker: (CoinType) 단일 티커
        :return
            float : (float) 소유량
        """
        return self.upbit.get_balance(ticker.label)

    def get_buy_average(self, ticker: CoinType) -> float:
        """본인이 매수한 특정 코인의 평균 매수가 조회
        :param ticker: (CoinType) 단일 티커
        :return
            float : 현재 가격 (원화)
        """
        return self.upbit.get_avg_buy_price(ticker)

    def get_order_info(self, ticker_or_uuid: str):
        """미체결 주문 정보 조회
        :param ticker_or_uuid: (CoinType) 단일 티커
        :return
            float : 현재 가격 (원화)
        """
        try:
            orders = self.upbit.get_order(ticker_or_uuid)
            if 'error' in orders[0]:
                print(f'occur error {orders[0]=}')
                return None
            return orders[-1]  # 마지막 주문건에 대한 정보
        except Exception as e:
            print(f'occur Exception error {e=}')
            return None

    def order_buy_market(self, ticker: CoinType, buy_amount: float):
        """시장가 매수
        :param ticker : (CoinType) 단일 티커
        :param buy_amount : 매수할 금액
        """
        if buy_amount < 5000:
            print(f'less than minimum order amount(5000won) {buy_amount=}')
            return 0
        try:
            res = self.upbit.buy_market_order(ticker, buy_amount)
            if 'error' in res:
                print(res)
                return 0
            print(res)
            return res
        except Exception as e:
            print('error 발생!!!!!!!!!!!!!!!!')
            print(e)
            return 0

    # 시장가 매도
    def order_sell_market(self, ticker: str, volume):
        """
        : ticker : 코인 이름
        : volume : 매도할 수량
        """
        try:
            res = self.upbit.sell_market_order(ticker, volume)
            if 'error' in res:
                print(res)
                res = 0
                return res
            print(res)
            return res
        except Exception as e:
            print('error 발생!!!!!!!!!!!!!!!!')
            print(e)
            return 0

    # 지정가 매수
    def order_buy_limit(self, ticker: str, price: float, volume):
        """
        : ticker : 코인 이름
        : price : 매수할 가격
        : volume : 매수할 수량
        """
        try:
            res = self.upbit.buy_limit_order(ticker, price, volume)
            if 'error' in res:
                print(res)
                return 0
            print(res)
            return res
        except Exception as e:
            print('error 발생!!!!!!!!!!!!!!!!')
            print(e)
            return 0

    # 지정가 매도
    def order_sell_limit(self, ticker: str, price: float, volume):
        """
        : ticker : 코인 이름
        : price : 매도할 가격
        : volume : 매도할 수량
        """
        try:
            res = self.upbit.sell_limit_order(ticker, price, volume)
            if 'error' in res:
                print(res)
                return 0
            print(res)
            return res
        except Exception as e:
            print('error 발생!!!!!!!!!!!!!!!!')
            print(e)
        return 0

    # 주문 취소
    def order_cancel(self, ticker):
        order_info = self.get_order_info(ticker)
        if order_info is None:
            return 0
        try:
            order_uuid = order_info['uuid']
            res = self.upbit.cancel_order(order_uuid)
            if 'error' in res:
                print(res)
                return 0
            print(res)
        except Exception as e:
            print(e)
        return 0

    # 볼린져 밴드(Bollinger band) 전략
    '''
        볼린져 밴드는 세 개의 선을 그리는 전략
        1) 중심 밴드 (Middle Band) : 주가의 단순 이동평균선이며, 20일 이동 평균을 사용
        2) 상단 밴드 (Upper Band) : 일반적으로 중심 밴드에서 2배의 표준 편차를 더한 값
        3) 하단 밴드 (Lower Band) : 중심 밴드에서 2배의 표준 편차를 뺀 값
    '''

    def get_bollinger_bands(self, prices, window: int = 20, multiplier: int = 2):
        '''
        :param prices: 가격 데이터
        :param window:  이동 평균을 계산하기 위한 기간
        :param multiplier: 상단 밴드와 하단 밴드를 계산할 때 사용되는 표준 편차의 배수
        '''

        ### 20일 동안 이동 평균선 계산 (Middle Band)
        sma = prices.rolling(window=window).mean()

        ### 20일 동안의 표준 편차 계산
        rolling_std = prices.rolling(window=window).std()

        ### 중간 밴트 + (표준 편차 * 2)
        upper_band = sma + (rolling_std * multiplier)

        ### 중간 밴트 - (표준 편차 * 2)
        lower_band = sma - (rolling_std * multiplier)

        return upper_band, lower_band

    def trading_signal(self, prices):
        ### get_bollinger_bands() 를 통해 상단/하단 밴드 요청
        upper_band, lower_band = self.get_bollinger_bands(prices)

        band_high = upper_band.iloc[-1]
        band_low = lower_band.iloc[-1]
        current_price = self.get_current_price(ticker='KRW-BTC')

        ### 상단 / 하단 / 현재가 출력
        log.log('DG', 'response', f'HIGH : {band_high} / LOW : {band_low} / PRICE : {current_price}')

        '''
            현재 가겨이 상단 밴드보다 큰 경우 'BUY 신호
            하단 밴드보다 낮은 경우는 'SELL' 신호
            밴드안에 있는 경우는 'HOLD' 신호 
        '''
        ret = 'HOLD'
        if current_price > band_high:
            print('SELL SIGNAL')
            ret = 'SELL'

        if current_price < band_low:
            print('BUY SIGNAL')
            ret = 'BUY'

        log.log('DG', 'response', 'Signal : ' + ret)
        return ret

    def trading(self, ticker: str):
        ### get_ohlcv 함수를 이용해서 업비트 사이트의 20일 데이터 받아오기
        price_data = pyupbit.get_ohlcv(ticker, interval='day', count=20)
        prices = price_data['close']

        ### 받아온 가격 데이터의 종가만을 추출 하여 trading_signal 호출
        signal = self.trading_signal(prices=prices)
        balance_cash = self.get_balance_cash()
        balance_coin = self.get_balance_coin(ticker=ticker)

        # 매수 금액
        buy_unit = calculate_trade_unit(balance_cash)

        log.log('TR', 'response', f'SIGNAL : {signal} / BALANCE COIN : {balance_coin} / BALANCE CASH : {balance_cash}')

        if balance_cash < 10_000:
            log.log('TR', 'response', '잔액 부족!!!!!!!')
            return None

        ret = None
        if signal == 'BUY' and balance_cash > buy_unit:
            ret = self.order_buy_market(ticker=ticker, buy_amount=10_000)
            log.log('TR', 'response', f'Buy Order : {ret}')
            return ret

        if signal == 'SELL' and balance_coin > 0:
            ret = self.order_sell_market(ticker=ticker, volume=balance_coin)
            log.log('TR', 'response', f'Sell Order : {ret}')
            return ret

        log.log('DG', 'response', 'Hold Position')
        return ret

    def run(self):
        ret = self.trading(ticker='KRW-BTC')
        if ret is not None:
            print(ret)

# uuid	주문의 고유 식별자
# side	주문 타입 ('ask'는 매도 / 'bid'는 매수 주문을 의미)
# ord_type	주문 유형 (예: 'limit'는 한도 주문을 의미)
# price	주문 가격
# state	주문 상태 (예: 'wait'는 대기 중인 주문을 의미)
# market	주문이 발생한 시장 (예: 'KRW-XRP'는 한국 원화로 리플을 거래하는 시장을 의미)
# created_at	주문 생성 시간
# volume	주문 수량
# remaining_volume	남아있는 주문량
# reserved_fee	예약된 수수료
# remaining_fee	남아있는 수수료
# paid_fee	지불된 수수료
# locked	locking 금액 또는 자산
# executed_volume	실행된 주문량
# trades_count	거래 횟수
