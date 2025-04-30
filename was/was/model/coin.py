from enum import auto

from was.ex.enum_ex import StringEnum


class MarketType(StringEnum):
    KRW = auto()
    KRW_BTC = auto()
    KRW_TRX = auto()
    KRW_GAS = auto()

    @property
    def label(self) -> str:
        match self:
            case MarketType.KRW_BTC:
                return 'KRW-BTC'
            case MarketType.KRW_TRX:
                return 'KRW-TRX'
            case MarketType.KRW_GAS:
                return 'KRW-GAS'
            case MarketType.KRW:
                return 'KRW'
            case _:
                return ''

    @property
    def currency(self) -> str:
        match self:
            case MarketType.KRW_BTC:
                return 'BTC'
            case MarketType.KRW_TRX:
                return 'TRX'
            case MarketType.KRW_GAS:
                return 'GAS'
            case MarketType.KRW:
                return 'KRW'
            case _:
                return ''
