from was.model.coin import MarketType
from was.service.upbit import get_ohlcv


def app():
    price_data = get_ohlcv(market=MarketType.KRW_BTC)
