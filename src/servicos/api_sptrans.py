from datetime import datetime
from typing import List, Optional, Final
from zoneinfo import ZoneInfo

import requests

from src.config.config import Config
from src.modelos.linhas import Linhas
from src.modelos.onibus import Onibus


class ApiSptrans:
    def __init__(self):
        self.__CHAVE = Config.CHAVE_API
        self.__URL = Config.URL_API_SPTRANS

    def __realizar_login(self) -> Optional[str]:
        url_completa: Final[str] = f'{self.__URL}Login/Autenticar?token={self.__CHAVE}'
        req = requests.post(url_completa)
        return req.cookies.get('apiCredentials')

    def __parse_onibus(self, v: dict) -> Onibus:
        ta_utc = datetime.fromisoformat(v["ta"].replace("Z", "+00:00"))
        ta_brasilia = ta_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
        return Onibus(
            p=v["p"],
            a=v["a"],
            ta=ta_brasilia,
            py=v["py"],
            px=v["px"],
            sv=v.get("sv"),
            is_=v.get("is"),
        )

    def __parse_linha(self, ln: dict) -> Linhas:
        return Linhas(
            c=ln["c"],
            cl=ln["cl"],
            sl=ln["sl"],
            lt0=ln["lt0"],
            lt1=ln["lt1"],
            qv=ln["qv"],
            vs=[self.__parse_onibus(v) for v in ln.get("vs", [])],
        )

    def buscar_linhas(self) -> List[Linhas]:
        cookie = self.__realizar_login()
        url_completa: Final[str] = f'{self.__URL}Posicao'
        headers = {'Cookie': f'apiCredentials={cookie}'}
        req = requests.get(url=url_completa, headers=headers)
        linhas_raw = req.json().get('l', [])
        return list(map(self.__parse_linha, linhas_raw))


if __name__ == '__main__':
    api_sptrans = ApiSptrans()
    linhas = api_sptrans.buscar_linhas()
    for linha in linhas:
        print(linha)
