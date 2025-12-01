import json

import requests

from src.config.config import Config


class KsqlApi:
    def __init__(self):
        self.__URL = Config.URL_KSQL

    def obter_posicao_atual(self, codigo_linha: str):
        url = self.__URL + '/query'
        payload = json.dumps({
            "ksql": f"SELECT C,PY,ID_ONIBUS, TA , PX FROM ONIBUS_POSICAO_ATUAL WHERE c = '{codigo_linha}';",
            "streamsProperties": {
                "auto.offset.reset": "latest"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        linhas = response.text.splitlines()

        dados_linhas = filter(lambda l: l.startswith('['), linhas)
        dados_listas = map(json.loads, dados_linhas)
        to_dict = lambda x: {
            "c": x[0],
            "py": x[1],
            "id_onibus": x[2],
            'ta': x[3],
            'px': x[4]
        }
        dados_dict = list(map(to_dict, dados_listas))
        print(dados_dict)
        return dados_dict
