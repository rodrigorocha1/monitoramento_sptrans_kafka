from datetime import datetime
from itertools import chain
from typing import List, Optional, Final

import requests

from src.config.config import Config
from src.modelos.linhas import Linhas


class ApiSptrans:
    def __init__(self):
        self.__CHAVE = Config.CHAVE_API
        self.__URL = Config.URL_API_SPTRANS

    def __realizar_login(self) -> Optional[str]:
        url_completa: Final[str] = f'{self.__URL}Login/Autenticar?token={self.__CHAVE}'
        req = requests.post(url_completa)
        return req.cookies.get('apiCredentials')

    def __desnormalizar_json(self, ln: dict) -> List[Linhas]:
        return list(
            map(
                lambda vs_item: Linhas(
                    c=ln.get('c'),
                    cl=ln.get('cl'),
                    sl=ln.get('cl'),
                    lt0=ln.get("lt0"),
                    lt1=ln.get("lt1"),
                    qv=ln.get("qv"),
                    p=vs_item.get("p"),
                    a=vs_item.get("a"),
                    ta=datetime.fromisoformat(vs_item.get("ta")),
                    py=vs_item.get("py"),
                    px=vs_item.get("px")

                ),
                ln["vs"]
            )
        )

    def buscar_linhas(self) -> List[Linhas]:
        cookie = self.__realizar_login()
        url_completa: Final[str] = f'{self.__URL}Posicao'
        headers = {'Cookie': f'apiCredentials={cookie}'}
        req = requests.get(url=url_completa, headers=headers)
        resposta = req.json()

        json_desnormalizado = list(chain.from_iterable(map(self.__desnormalizar_json, resposta['l'])))

        return json_desnormalizado


if __name__ == '__main__':
    api_sptrans = ApiSptrans()
    linhas = api_sptrans.buscar_linhas()
    print(linhas[0: 2])
    for linha in linhas[0: 2]:
        print(linha)
