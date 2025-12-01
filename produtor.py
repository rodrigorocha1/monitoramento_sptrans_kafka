import json
from datetime import datetime
from time import sleep

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

from src.config.config import Config
from src.modelos.linha import Linha
from src.servicos.api_sptrans import ApiSptrans


class Produtor:
    def __init__(self):
        self.__URL_KAFKA = Config.URL_KAFKA
        self.__produtor = KafkaProducer(
            bootstrap_servers=self.__URL_KAFKA,
            value_serializer=lambda v: json.dumps(v, default=self.__json_serializer, ensure_ascii=False).encode(
                'utf-8'),
            key_serializer=lambda k: k.encode('utf-8'),

        )
        self.__admin_cliente = KafkaAdminClient(
            bootstrap_servers=self.__URL_KAFKA
        )
        self.__req_api_sptrans = ApiSptrans()
        self.__num_particoes = 6
        self.__replication_factor = 1
        self.__topico = 'linhas_onibus'
        self.__criar_topico()

    def __criar_topico(self):
        """
        Método para criar tópico do kafka

        """
        novo_topico = NewTopic(
            name=self.__topico,
            num_partitions=self.__num_particoes,
            replication_factor=self.__replication_factor
        )
        try:
            self.__admin_cliente.create_topics([novo_topico])
            print(f"Tópico '{self.__topico}' criado com {self.__num_particoes} partições.")
        except TopicAlreadyExistsError:
            print(f"Tópico '{self.__topico}' já existe.")

    def __enviar_dados(self, codigo_linha: str, dados: Linha):
        """
        método para enviar dados ao kafka
        :param codigo_linha: código da linha do ônibus
        :type codigo_linha: str
        :param dados: dados da Linha de ônubibos
        :type dados: Linna

        """
        self.__produtor.send(
            topic=self.__topico,
            value=dados,
            key=codigo_linha
        )

    def rodar_produtor(self, intervalo: int = 30):
        """
        Método para rodar o produtor kafka
        :param intervalo: intervalo de tempo de delay
        :type intervalo: int

        """
        print("Iniciando produtor Kafka...")
        while True:
            dados_linhas = self.__req_api_sptrans.buscar_linhas()
            codigo_linha = 'linhas_sptrans'
            for linha in dados_linhas:
                self.__enviar_dados(codigo_linha, linha)
                self.__produtor.flush()
            sleep(intervalo)

    @staticmethod
    def __json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f'Tipo {type(obj)} não serializável')


if __name__ == '__main__':
    produtor = Produtor()
    produtor.rodar_produtor(intervalo= 2 * 60)
