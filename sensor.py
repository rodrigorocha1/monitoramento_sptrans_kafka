import json
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

from src.config.config import Config

# Configurações do Kafka
KAFKA_BROKER = Config.URL_KAFKA # Alterar se necessário
TOPIC_NAME = 'sensor_temperatura'

# Cria o produtor Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def gerar_leitura_sensor():
    """
    Simula leitura de sensor de temperatura com timestamp em UTC ISO 8601
    compatível com ksqlDB (sem Z no final, microsegundos incluídos)
    """
    timestamp = datetime.now(timezone.utc).replace(tzinfo=None).isoformat(timespec='microseconds')
    return {
        "sensor_id": "sensor_001",
        "temperatura": round(random.uniform(20.0, 30.0), 2),
        "timestamp": timestamp
    }

def enviar_dados():
    while True:
        leitura = gerar_leitura_sensor()
        producer.send(TOPIC_NAME, value=leitura)
        print(f"Enviado: {leitura}")
        time.sleep(2)

if __name__ == "__main__":
    print(f"Iniciando sensor e enviando dados para '{TOPIC_NAME}'...")
    enviar_dados()