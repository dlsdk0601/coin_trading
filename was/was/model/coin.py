from enum import auto

from was.ex.enum_ex import StringEnum


class MarketType(StringEnum):
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
            case _:
                return ''
