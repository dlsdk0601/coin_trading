import pyupbit
from pyupbit import Upbit

import config


class Upbit:
    upbit: Upbit

    def __init__(self):
        upbit = Upbit(config.UPBIT_ACCESS_KEY, config.UPBIT_SECRET_KEY)

    # 현재 보유 금액 조회
    def get_balance_cash(self):
        return self.upbit.get_balance('KRW')

    # 현재가격 조회
    def get_current_price(self, ticker: str):
        return pyupbit.get_current_price(ticker)

    # 현재 코인 보유 수량 조회
    def get_balance_coin(self, ticker: str):
        return self.upbit.get_balance(ticker)

    # 평균 매수가 조회
    def get_buy_average(self, ticker: str):
        return self.upbit.get_avg_buy_price(ticker)


   # 주문 (미체결)정보 조회
   def get_order_info(self, ticker_or_uuid: str):
       try:
           orders = self.upbit.get_order(ticker_or_uuid)
           if 'error' in orders[0]:
               print('error 발생!!!!!!!!!!!!!!!!')
               return None
           return orders[-1] # 마지막 주문건에 대한 정보
       except Exception as e:
           print('error 발생!!!!!!!!!!!!!!!!')
           print(e)
           return None

    # 시장가 매수
    def order_buy_market(self, ticker: str, buy_amount: float):
        """
        : ticker : 코인 이름
        : buy_amount : 매수할 금액
        """
        if buy_amount < 5000:
            print('주문 최소 금액보다 작습니다(5000원)')
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