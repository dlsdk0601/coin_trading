from was.ex.calculate_ex import get_margin
from was.ex.logger import log, LogLevel
from was.model import db
from was.model.coin import MarketType
from was.model.config import Config
from was.service.upbit import bollinger_trading, upbit_current_deposit, upbit_current_ticker


def _serve():
    try:
        target_market = MarketType.KRW_BTC
        target_unit = MarketType.KRW

        # 볼린저 밴드를 구해서 BUY / SELL / HOLD 중 하나를 한다.
        res = bollinger_trading(market=target_market)

        # 현재 보유 현금 (소수 1번째 반올림)
        current_cash_res = upbit_current_deposit(req=target_unit)
        current_cash = float(current_cash_res.balance) if current_cash_res is not None else 0

        # 현재 코인 가격
        current_price_res = upbit_current_ticker(req=target_market)
        current_price = current_price_res.trade_price if current_price_res is not None else 0

        # 현재 코인 보유 수량 (소수 3번째 반올림)
        current_balance_res = upbit_current_deposit(req=target_market)
        current_balance = round(float(current_balance_res.balance) if current_balance_res is not None else 0, 2)

        # 평균 매수 가격
        buy_avg_price = float(current_balance_res.avg_buy_price) if current_balance_res is not None else 0

        # 평가 손익 / 수익률
        margin, margins = get_margin(current_price, buy_avg_price, current_balance)

        log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | 잔액 : {current_cash:,d}원')  # ',d'는 천 단위 구분자 추가
        log.log(level=LogLevel.INFO,
                text=f'UPBIT | BOLLINGER BAND | 보유량 : {current_balance:,.2f} market={MarketType.KRW_BTC.label}')
        log.log(level=LogLevel.INFO,
                text=f'UPBIT | BOLLINGER BAND | 평단가 : {buy_avg_price:,.2f}원')  # '.2f'는 소수점 아래 두 자리까지 표시
        log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | 현재가 : {current_price:,.2f}원')
        log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | 수익률 : {margins:,.2f}%')  # 소수점 아래 두 자리 수익률
        log.log(level=LogLevel.INFO, text=f'UPBIT | BOLLINGER BAND | 수익금 : {int(round(margin, 0)):,d}원')

        if res is not None:
            log.log(level=LogLevel.WARNING, text=f'UPBIT | BOLLINGER BAND | RES IS NULL')

    except ZeroDivisionError as Div_zero:
        log.log(level=LogLevel.ERROR, text=f'UPBIT | BOLLINGER BAND | ZERO DIVISION ERROR | {Div_zero=}')
    except Exception as e:
        log.log(level=LogLevel.ERROR, text=f'UPBIT | BOLLINGER BAND | EXCEPTION | {e=}')


if __name__ == '__main__':
    emergency_q = db.select(Config).filter(Config.key == 'emergency')
    emergency = db.session.execute(emergency_q).scalar_one_or_none()

    if emergency is not None:
        if emergency == 'false':
            _serve()
