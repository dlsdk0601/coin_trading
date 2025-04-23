import time

from was import config
from was.main import app
from was.model.coin import CoinType
from was.repository.upbit import UpbitData

if __name__ == '__main__':
    upbit = UpbitData()
    res = upbit.get_buy_average(ticker=CoinType.KRW_TRX)
    print(type(res))
    print(res)

    # if config.IS_LOOP:
    #     while True:
    #         app()
    #         time.sleep(3.5)
    # else:
    #     app()