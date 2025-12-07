import json

from src.models.consulta import Consulta
from src.servicos.ksql_api import KsqlApi


class DashboardController:

    def __init__(self):
        self.__consulta = Consulta()
        self.__ksql_api = KsqlApi()

    def obter_nome_linha(self, codigo_linha: str):
        sql = """
        select r.route_long_name 
        FROM routes r   
        where r.route_id  = :codigo
        """
        resultado = self.__consulta.consulta(sql=sql, params={"codigo": codigo_linha})

        return resultado

    def rodar_consulta_trajeto_onibus(self, codigo_linha: str):
        sql_viagem = """
            select  s.shape_pt_lat , s.shape_pt_lon , r.route_color 
            FROM trips t 
            INNER JOIN routes r on r.route_id  = t.route_id 
            INNER JOIN shapes s  on s.shape_id  = t.shape_id
            where r.route_id  = :codigo
            order by t.direction_id , s.shape_pt_sequence 
;
        """
        resultado = self.__consulta.consulta(sql_viagem, {"codigo": codigo_linha})
        return resultado

    def obter_posicao_atual(self, codigo_linha: str):
        sql = f"""
            SELECT C,PY,ID_ONIBUS, TA , PX 
            FROM ONIBUS_POSICAO_ATUAL WHERE c = '{codigo_linha}';
        """

        response = self.__ksql_api.executar_consulta(sql=sql)
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

        return dados_dict

    def obter_velocidade_onibus(self, codigo_linha: str):
        sql = f"""
            SELECT
            C,
            S_P,
            curr_ta,
            ROUND(
                  velocidade_media(
                    CAST(prev_py AS DECIMAL(9,6)),
                    CAST(prev_px AS DECIMAL(9,6)),
                    CAST(curr_py AS DECIMAL(9,6)),
                    CAST(curr_px AS DECIMAL(9,6)),
                    CONCAT(prev_ta,'Z'),
                    CONCAT(curr_ta,'Z')
                        ), 2
                    ) AS VELOCIDADE_KMH
            FROM ONIBUS_POSICAO_ANTERIOR_ATUAL
            WHERE curr_ta IS NOT NULL AND PREV_PY is not null 
            AND C = '{codigo_linha}';
            """
        response = self.__ksql_api.executar_consulta(sql=sql)
        linhas = response.text.splitlines()
        dados_onibus = filter(lambda l: l.startswith('['), linhas)
        dados_onibus = map(json.loads, dados_onibus)
        to_dict = lambda x: {
            "CODIGO_LINHA": x[0],
            "CODIGO_ONIBUS": x[1],
            "TEMPO_ATUAL": x[2],
            'VELOCIDADE KMH': x[3],
        }
        dados_dict = list(map(to_dict, dados_onibus))
        return dados_dict

