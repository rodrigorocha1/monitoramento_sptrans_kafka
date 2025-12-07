import json

import requests

from src.config.config import Config


class KsqlApi:
    def __init__(self):
        self.__URL = Config.URL_KSQL

    def executar_consulta(self, sql: str):
        url = self.__URL + '/query'
        payload = json.dumps({
            "ksql":sql,
            "streamsProperties": {
                "auto.offset.reset": "latest"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)

        return response
