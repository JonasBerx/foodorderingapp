from typing import Any, List, Optional

from dolt.models import Order


def get_float(obj: Any) -> Optional[float]:
    try:
        return round(float(obj), 2)
    except ValueError:
        return None


def get_unfinished_orders() -> List[Order]:
    ongoing_orders = Order.query.filter(Order.status == "ongoing").all()
    delivering_orders = Order.query.filter(Order.status == "delivering").all()
    cancelled_orders = Order.query.filter(Order.status == "cancelled").all()
    available_orders = ongoing_orders[::-1] + delivering_orders[::-1] + cancelled_orders[::-1]
    return available_orders
