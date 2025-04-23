from enum import auto

from was.ex.enum_ex import StringEnum


class CoinType(StringEnum):
    KRW_BTC = auto()
    KRW_TRX = auto()
    KRW_GAS = auto()

    @property
    def label(self) -> str:
        match self:
            case CoinType.KRW_BTC:
                return 'KRW-BTC'
            case CoinType.KRW_TRX:
                return 'KRW-TRX'
            case CoinType.KRW_GAS:
                return 'KRW-GAS'
            case _:
                return ''