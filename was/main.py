import time

from src.logger import log
from src.upbit import UpbitData

coin = 'KRW-BTC'


def get_margin(current_price, buy_avg_price, current_balance):
    margin_rate = float((current_price - buy_avg_price) / buy_avg_price) * 100.0
    margin = current_balance * buy_avg_price * (margin_rate / 100.0)
    return margin, margin_rate


def main():
    upbit = UpbitData()
    try:
        # BUY / SELL / HOLD 결정
        ret = upbit.trading(ticker=coin)

        # 현재 보유 현금 (소수 1번째 반올림)
        current_cash = int(round(upbit.get_balance_cash(), 0))

        # 현재 코인 가격
        current_price = upbit.get_current_price(ticker=coin)

        # 현재 코인 보유 수량 (소수 3번째 반올림)
        current_balance = round(upbit.get_balance_coin(ticker=coin), 2)

        # 평균 매수 가격
        buy_avg_price = upbit.get_buy_average(ticker=coin)

        # 평가 손익 / 수익률
        margin, margins = get_margin(current_price, buy_avg_price, current_balance)

        log.log('TR', f'  잔액 : {current_cash:,d}원')  # ',d'는 천 단위 구분자 추가
        log.log('TR', f'보유량 : {current_balance:,.2f} {coin}')
        log.log('TR', f'평단가 : {buy_avg_price:,.2f}원')  # '.2f'는 소수점 아래 두 자리까지 표시
        log.log('TR', f'현재가 : {current_price:,.2f}원')
        log.log('TR', f'수익률 : {margins:,.2f}%')  # 소수점 아래 두 자리 수익률
        log.log('TR', f'수익금 : {int(round(margin, 0)):,d}원')

        if ret is not None:
            print(ret)

    except ZeroDivisionError as Div_zero:
        log.log('WA', '보유 코인 수 확인', Div_zero)
    except Exception as e:
        log.log('DG', 'Running Error', e)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(secs=60)
