import hashlib
import uuid
from dataclasses import dataclass
from enum import auto
from typing import Any, Tuple
from urllib.parse import unquote, urlencode

import jwt
import requests
from requests import Response

from was import config
from was.ex.enum_ex import StringEnum
from was.ex.logger import log, LogLevel
from was.model.coin import MarketType


@dataclass
class Err:
    name: str
    message: str


@dataclass
class GetAccountResItem:
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    balance: str  # 주문 가능 금액/수량
    locked: str  # 주문 중 묶여 있는 금액/수량
    avg_buy_price: str  # 매수평균가
    avg_buy_price_modified: bool  # 매수평균가 수정 여부
    unit_currency: str  # 평단가 기준 화폐


@dataclass
class GetAccountRes:
    accounts: list[GetAccountResItem]


def get_account() -> GetAccountRes | Err:
    """전체 계좌 조회
    :return: GetAccountRes | None (코인별 정보 리스트)
    """
    res_or_err = _upbit_request(path='/accounts', params={}, method=RequestMethod.GET)

    if isinstance(res_or_err, Err):
        return res_or_err

    accounts = [GetAccountResItem(**item) for item in res_or_err]
    return GetAccountRes(accounts=accounts)


@dataclass
class GetOrderChanceReq:
    market: MarketType


@dataclass
class GetOrderChanceResMarketBid:
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    min_total: float  # 최소 매도/매수 금액


@dataclass
class GetOrderChanceResMarketAsk:
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    min_total: float  # 최소 매도/매수 금액


@dataclass
class GetOrderChanceResMarket:
    id: str  # 마켓의 유일 키
    name: str  # 마켓 이름
    order_types: list[str]  # 지원 주문 방식 (만료)
    ask_types: list[str]  # 매도 주문 지원 방식
    bid_types: list[str]  # 매수 주문 지원 방식
    order_sides: list[str]  # 지원 주문 종류
    max_total: str  # 최대 매도/매수 금액
    state: str  # 마켓 운영 상태
    bid: GetOrderChanceResMarketBid  # 매수 시 제약 사항
    ask: GetOrderChanceResMarketAsk  # 매도 시 제약 사항


@dataclass
class GetOrderChanceResBidAccount:
    currency: str  # 화폐를 의미 하는 영문 대문자 코드
    balance: str  # 주문 가능 금액/수량
    locked: str  # 주문 중 묶여 있는 금액/수량
    avg_buy_price: str  # 매수 평균가
    avg_buy_price_modified: bool  # 매수 평균가 수정 여부
    unit_currency: str  # 평단가 기준 화폐


@dataclass
class GetOrderChanceResAskAccount:
    currency: str  # 화폐를 의미 하는 영문 대문자 코드
    balance: str  # 주문 가능 금액/수량
    locked: str  # 주문 중 묶여 있는 금액/수량
    avg_buy_price: str  # 매수 평균가
    avg_buy_price_modified: bool  # 매수 평균가 수정 여부
    unit_currency: str  # 평단가 기준 화폐


@dataclass
class GetOrderChanceRes:
    bid_fee: str  # 매수 수수료 비율
    ask_fee: str  # 매도 수수료 비율
    maker_bid_fee: str
    maker_ask_fee: str
    market: GetOrderChanceResMarket  # 마켓에 대한 정보
    bid_account: GetOrderChanceResBidAccount  # 매수 시 사용 하는 화폐의 계좌 상태
    ask_account: GetOrderChanceResAskAccount  # 매도 시 사용하는 화폐의 계좌 상태


def get_orders_chance(req: GetOrderChanceReq) -> GetOrderChanceRes | Err:
    """주문 가능 정보
    :return: GetOrderChanceRes | None (코인별 정보 리스트)
    """
    params = {
        'market': req.market.label,
    }
    res_or_err = _upbit_request(path='/orders/chance', params=params, method=RequestMethod.GET)

    if isinstance(res_or_err, Err):
        return res_or_err

    return GetOrderChanceRes(**res_or_err)


@dataclass
class OrderBuyMarketReq:
    market: MarketType  # 마켓 ID
    price: float  # 주문 가격 (시장가)


@dataclass
class OrderMarketRes:
    # 주문의 고유 아이디
    uuid: str
    # 주문 종류 (bid: 매수, ask: 매도)
    side: str
    # 주문 방식
    # - limit : 지정가 주문
    # - price : 시장가 주문(매수)
    # - market : 시장가 주문(매도)
    # - best : 최유리 주문 (time_in_force 설정 필수)
    ord_type: str
    # 주문 당시 화폐 가격
    price: str
    # 주문 상태
    state: str
    # 마켓의 유일키	(MarketType)
    market: str
    # 주문 생성 시간
    created_at: str
    # 사용자가 입력한 주문 양
    volume: str
    # 체결 후 남은 주문 양
    remaining_volume: str
    # 수수료로 예약된 비용
    reserved_fee: str
    # 남은 수수료
    remaining_fee: str
    # 사용된 수수료
    paid_fee: str
    # 거래에 사용중인 비용
    locked: str
    # 체결된 양
    executed_volume: str
    # 해당 주문에 걸린 체결 수
    trades_count: int
    # IOC, FOK 설정	String
    time_in_force: str
    # 조회용 사용자 지정값
    identifier: str


def order_buy_market(req: OrderBuyMarketReq) -> OrderMarketRes | Err:
    """시장가 매수
    :return: OrderMarketRes | ERR
    """
    params = {
        'market': req.market.label,
        'side': 'bid',
        'price': str(req.price),
        'ord_type': 'price',
    }

    res_or_error = _upbit_request(path='/orders', params=params, method=RequestMethod.POST)

    if isinstance(res_or_error, Err):
        return res_or_error

    return OrderMarketRes(**res_or_error)

@dataclass
class OrderSellMarketReq:
    market: MarketType  # 마켓 ID
    volume: float  # 주문 가격 (시장가)

def order_sell_market(req: OrderSellMarketReq) -> OrderMarketRes | Err:
    """시장가 매도
    :return: OrderMarketRes | ERR
    """
    params = {
        'market': req.market.label,
        'side': 'ask',
        'volume': str(req.volume),
        'ord_type': 'market',
    }

    res_or_error = _upbit_request(path='/orders', params=params, method=RequestMethod.POST)

    if isinstance(res_or_error, Err):
        return res_or_error

    return OrderMarketRes(**res_or_error)


@dataclass
class GetCandleDayReq:
    market: MarketType
    to: str
    count: int
    converting_price_unit: str = 'KRW'


@dataclass
class GetCandleDayResItem:
    market: str  # 종목 코드
    candle_date_time_utc: str  # 캔들 기준 시각(UTC 기준) 포맷: yyyy-MM-ddTHH:mm:ss
    candle_date_time_kst: str  # 캔들 기준 시각(KST 기준) 포맷: yyyy-MM-ddTHH:mm:ss
    opening_price: float  # 시가
    high_price: float  # 고가
    low_price: float  # 저가
    trade_price: float  # 종가
    timestamp: int  # 마지막 틱이 저장된 시각
    candle_acc_trade_price: float  # 누적 거래 금액
    candle_acc_trade_volume: float  # 누적 거래량
    prev_closing_price: float  # 전일 종가(UTC 0시 기준)
    change_price: float  # 전일 종가 대비 변화 금액
    change_rate: float  # 전일 종가 대비 변화량
    converted_trade_price: float  # 종가 환산 화폐 단위로 환산된 가격(요청에 convertingPriceUnit 파라미터 없을 시 해당 필드 포함되지 않음.)


@dataclass
class GetCandleDayRes:
    candles: list[GetCandleDayResItem]


def get_candle_day(req: GetCandleDayReq) -> GetCandleDayRes | Err:
    """시세 캔들 조회 (일별)
    :return: GetCandleDayRes | ERR
    """
    params = {
        'market': req.market.label,
        'count': req.count,
        'to': req.to,
        'converting_price_unit': req.converting_price_unit,
    }
    res_or_error = _upbit_request(path='/candles/days', params=params, method=RequestMethod.GET)
    if isinstance(res_or_error, Err):
        return res_or_error

    candles = [GetCandleDayResItem(**item) for item in res_or_error]
    return GetCandleDayRes(candles=candles)


@dataclass
class GetTickerReq:
    markets: list[MarketType]


@dataclass
class GetTickerResItem:
    market: str  # 종목 구분 코드
    trade_date: str  # 최근 거래 일자(UTC) 포맷: yyyyMMdd
    trade_time: str  # 최근 거래 시각(UTC) 포맷: HHmmss
    trade_date_kst: str  # 최근 거래 일자(KST) 포맷: yyyyMMdd
    trade_time_kst: str  # 최근 거래 시각(KST) 포맷: HHmmss
    trade_timestamp: int  # 최근 거래 일시(UTC) 포맷: Unix Timestamp
    opening_price: float  # 시가
    high_price: float  # 고가
    low_price: float  # 저가
    trade_price: float  # 종가(현재가)
    prev_closing_price: float  # 전일 종가(UTC 0시 기준)
    change: str  # EVEN : 보합, RISE : 상승, FALL : 하락
    change_price: float  # 변화액의 절대값
    change_rate: float  # 변화율의 절대값
    signed_change_price: float  # 부호가 있는 변화액
    signed_change_rate: float  # 부호가 있는 변화율
    trade_volume: float  # 가장 최근 거래량
    acc_trade_price: float  # 누적 거래대금(UTC 0시 기준)
    acc_trade_price_24h: float  # 24시간 누적 거래대금
    acc_trade_volume: float  # 누적 거래량(UTC 0시 기준)
    acc_trade_volume_24h: float  # 24시간 누적 거래량
    highest_52_week_price: float  # 52주 신고가
    highest_52_week_date: str  # 52주 신고가 달성일 포맷: yyyy-MM-dd
    lowest_52_week_price: float  # 52주 신저가
    lowest_52_week_date: str  # 52주 신저가 달성일 포맷: yyyy-MM-dd
    timestamp: int  # 타임스탬프


@dataclass
class GetTickerRes:
    tickers: list[GetTickerResItem]


def get_ticker(req: GetTickerReq) -> GetTickerRes | Err:
    """종목 현재가 정보
    :return: GetTickerRes | ERR
    """
    params = {
        'market': ','.join([market.label for market in req.markets]),
    }
    res_or_error = _upbit_request(path='/ticker', params=params, method=RequestMethod.GET)
    if isinstance(res_or_error, Err):
        return res_or_error

    tickers = [GetTickerResItem(**item) for item in res_or_error]
    return GetTickerRes(tickers=tickers)


class RequestMethod(StringEnum):
    GET = auto()
    POST = auto()
    DELETE = auto()


def _upbit_request(path: str, params: dict[str, Any], method: RequestMethod):
    log.log(level=LogLevel.INFO, text=f'request : {method=}, {path=}, {params=}')

    server_url, headers = _get_api_element(path=path, params=params)

    res: Response | None = None
    match method:
        case RequestMethod.GET:
            res = requests.get(server_url, headers=headers, params=params)
        case RequestMethod.POST:
            res = requests.get(server_url, headers=headers, json=params)
        case RequestMethod.DELETE:
            res = requests.delete(server_url, headers=headers, params=params)

    if res is None:
        raise ValueError(f'res is None {res=}')

    if res.status_code != 200:
        err = res.json()
        return Err(name=err.name, message=err.message)

    return res.json()


def _get_api_element(path: str, params: dict[str, Any]) -> Tuple[str, dict[str, str]]:
    headers = _get_headers(params=params)
    server_url = config.API_URL
    if path.startswith('/'):
        server_url += path
    else:
        server_url += '/' + path

    return server_url, headers


def _get_headers(params: dict[str, Any]) -> dict[str, str]:
    authorization = _get_jwt_token(params=params)
    return {'Authorization': authorization}


def _get_jwt_token(params: dict[str, Any]) -> str:
    nonce = str(uuid.uuid4())
    query = unquote(urlencode(params, doseq=True)).encode('utf-8')
    m = hashlib.sha512()
    m.update(query)
    query_hash = m.hexdigest()

    payload = {
        'access_key': config.UPBIT_ACCESS_KEY,
        'nonce': nonce,
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    token = jwt.encode(payload, config.UPBIT_SECRET_KEY)
    return 'Bearer {}'.format(token)
