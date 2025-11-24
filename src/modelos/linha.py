from datetime import datetime
from typing import TypedDict


class Linha(TypedDict):
    c: str
    cl: int
    sl: int
    lt0: str
    lt1: str
    qv: int
    p: int
    a: bool
    ta: str
    py: float
    px: float
