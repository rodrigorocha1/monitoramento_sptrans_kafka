from typing import List, TypedDict

from src.modelos.onibus import Onibus


class Linhas(TypedDict):
    c: str
    cl: int
    sl: int
    lt0: str
    lt1: str
    qv: int
    vs: List[Onibus]
