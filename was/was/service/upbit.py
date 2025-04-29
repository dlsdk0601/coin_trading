from was.model.coin import MarketType
from was.repository import upbit


def upbit_current(req: MarketType):
    res = upbit.get_account()

    krw_account: upbit.GetAccountResItem | None = None
    match res:
        case upbit.Err(name=name, message=message):
            print(f'error :: {name=} {message=}')
            return None
        case upbit.GetAccountRes(accounts=accounts):
            acc: upbit.GetAccountResItem
            for acc in accounts.accounts:
                if acc.currency == req.label:
                    krw_account = acc

    return krw_account
