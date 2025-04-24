from was.model.coin import MarketType
from was.repository.upbit import get_orders_chance, GetOrderChanceReq

if __name__ == '__main__':
    res = get_orders_chance(GetOrderChanceReq(market=MarketType.KRW_BTC))
    print(f'res={res}')
