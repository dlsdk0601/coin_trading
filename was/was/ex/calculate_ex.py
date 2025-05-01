# 보유 현금에 따른 매수금액 지정
from typing import Tuple


def calculate_trade_unit(cash: float) -> float:
    if cash <= 300_000:
        return 6_000

    if 300_000 < cash <= 1_000_000:
        return 10_000

    if 1_000_000 < cash <= 1_500_000:
        return 15_000

    if 1_500_000 < cash <= 2_000_000:
        return 20_000

    if 2_000_000 < cash <= 3_000_000:
        return 25_000

    if 3_000_000 < cash <= 4_000_000:
        return 35_000

    if 4_000_000 < cash <= 8_000_000:
        return 50_000

    if 8_000_000 < cash:
        return 100_000

    return 0


def get_margin(current_price: float, buy_avg_price: float, current_balance: float) -> Tuple[float, float]:
    margin_rate = float((current_price - buy_avg_price) / buy_avg_price) * 100.0
    margin = current_balance * buy_avg_price * (margin_rate / 100.0)
    return margin, margin_rate
