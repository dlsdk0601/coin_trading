import hashlib
import uuid
from enum import auto
from typing import Any, Tuple
from urllib.parse import unquote, urlencode

import jwt
import requests
from requests import Response

from was import config
from was.ex.enum_ex import StringEnum
from was.ex.pydantic_ex import BaseModel
from was.model.coin import MarketType


class GetAccountResItem(BaseModel):
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    balance: str  # 주문 가능 금액/수량
    locked: str  # 주문 중 묶여 있는 금액/수량
    avg_buy_price: str  # 매수평균가
    avg_buy_price_modified: bool  # 매수평균가 수정 여부
    unit_currency: str  # 평단가 기준 화폐


class GetAccountRes(BaseModel):
    accounts: list[GetAccountResItem]


def get_account() -> GetAccountRes | None:
    """전체 계좌 조회
    :return: GetAccountRes | None (코인별 정보 리스트)
    """
    res = _upbit_request(path='/accounts', params={}, method=RequestMethod.GET)

    if res is None:
        return None

    return GetAccountRes(accounts=res)


class GetOrderChanceReq(BaseModel):
    market: MarketType


class GetOrderChanceResMarketBid(BaseModel):
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    min_total: float  # 최소 매도/매수 금액


class GetOrderChanceResMarketAsk(BaseModel):
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    min_total: float  # 최소 매도/매수 금액


class GetOrderChanceResMarket(BaseModel):
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


class GetOrderChanceResBidAccount(BaseModel):
    currency: str  # 화폐를 의미 하는 영문 대문자 코드
    balance: str  # 주문 가능 금액/수량
    locked: str  # 주문 중 묶여 있는 금액/수량
    avg_buy_price: str  # 매수 평균가
    avg_buy_price_modified: bool  # 매수 평균가 수정 여부
    unit_currency: str  # 평단가 기준 화폐


class GetOrderChanceResAskAccount(BaseModel):
    currency: str  # 화폐를 의미 하는 영문 대문자 코드
    balance: str  # 주문 가능 금액/수량
    locked: str  # 주문 중 묶여 있는 금액/수량
    avg_buy_price: str  # 매수 평균가
    avg_buy_price_modified: bool  # 매수 평균가 수정 여부
    unit_currency: str  # 평단가 기준 화폐


class GetOrderChanceRes(BaseModel):
    bid_fee: str  # 매수 수수료 비율
    ask_fee: str  # 매도 수수료 비율
    maker_bid_fee: str
    maker_ask_fee: str
    market: GetOrderChanceResMarket  # 마켓에 대한 정보
    bid_account: GetOrderChanceResBidAccount  # 매수 시 사용 하는 화폐의 계좌 상태
    ask_account: GetOrderChanceResAskAccount  # 매도 시 사용하는 화폐의 계좌 상태


def get_orders_chance(req: GetOrderChanceReq) -> GetOrderChanceRes | None:
    """주문 가능 정보
    :return: GetOrderChanceRes | None (코인별 정보 리스트)
    """
    params = {
        'market': req.market.label,
    }
    res = _upbit_request(path='/orders/chance', params=params, method=RequestMethod.GET)

    if res is None:
        return None

    return GetOrderChanceRes(**res)


class OrderBuyMarketReq(BaseModel):
    market: MarketType  # 마켓 ID
    price: float  # 주문 가격 (시장가)


class OrderBuyMarketRes(BaseModel):
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


def order_buy_market(req: OrderBuyMarketReq) -> OrderBuyMarketRes | None:
    params = {
        'market': req.market.label,
        'side': 'bid',
        'price': str(req.price),
        'ord_type': 'price',
    }

    res = _upbit_request(path='/orders', params=params, method=RequestMethod.POST)

    if res is None:
        return None

    return OrderBuyMarketRes(**res)


class RequestMethod(StringEnum):
    GET = auto()
    POST = auto()
    DELETE = auto()


def _upbit_request(path: str, params: dict[str, Any], method: RequestMethod):
    print(f'request : {method=}, {path=}, {params=}')

    server_url, headers = _get_api_element(path=path, params=params)

    res: Response | None = None
    match method:
        case RequestMethod.GET:
            res = requests.get(server_url, headers=headers, params=params)
        case RequestMethod.POST:
            res = requests.get(server_url, headers=headers, json=params)
        case RequestMethod.DELETE:
            res = requests.delete(server_url, headers=headers, params=params)

    # TODO :: 일단 에러 raise 하지 말고 None 처리, 후에 시스템 실행 시킬때 상황 보고 수정
    if res is None:
        print(f'res is nil')
        return None

    if res.status_code != 200:
        status_code = res.status_code
        error = res.json()
        print(f'{status_code=}, {error=}')
        return None

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
