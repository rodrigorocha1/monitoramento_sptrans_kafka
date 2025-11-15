from datetime import datetime
from itertools import chain
from typing import List, Optional, Final

import requests

from src.config.config import Config
from src.modelos.linha import Linha


class ApiSptrans:
    def __init__(self):
        self.__CHAVE = Config.CHAVE_API
        self.__URL = Config.URL_API_SPTRANS

    def __realizar_login(self) -> Optional[str]:
        """
        Método para fazer o login
        :return: cookies
        :rtype: Optional[str]
        """
        url_completa: Final[str] = f'{self.__URL}Login/Autenticar?token={self.__CHAVE}'
        req = requests.post(url_completa)
        return req.cookies.get('apiCredentials')

    def __desnormalizar_json(self, ln: dict) -> List[Linha]:
        return list(
            map(
                lambda vs_item: Linha(
                    c=ln["c"],
                    cl=ln["cl"],
                    sl=ln["sl"],
                    lt0=ln["lt0"],
                    lt1=ln["lt1"],
                    qv=ln["qv"],
                    p=vs_item["p"],
                    a=vs_item["a"],
                    ta=datetime.fromisoformat(vs_item["ta"]),
                    py=vs_item["py"],
                    px=vs_item["px"]

                ),
                ln["vs"]
            )
        )

    def buscar_linhas(self) -> List[Linha]:
        """
        Método para buscar todas as linhas da api da sptrans
        :return: Lista com todas as linha
        :rtype: List[Linha]
        """
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
