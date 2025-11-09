from datetime import datetime
from typing import Optional, TypedDict


class Onibus(TypedDict):
    p: int
    a: bool
    ta: datetime
    py: float
    px: float
    sv: Optional[str]
    is_: Optional[str]
