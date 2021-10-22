from typing import Any, Optional


def get_float(obj: Any) -> Optional[float]:
    try:
        return round(float(obj), 2)
    except ValueError:
        return None
