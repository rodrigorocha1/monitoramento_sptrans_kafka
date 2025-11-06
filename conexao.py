from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import time

TOPIC = "teste_conexao"
BOOTSTRAP_SERVERS = ["172.28.0.11:9092"]  # IP e porta do seu container Kafka

def testar_produtor():
    print("🔹 Testando envio de mensagens para o Kafka...")
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: v.encode("utf-8")
        )
        for i in range(5):
            msg = f"mensagem_teste_{i}"
            producer.send(TOPIC, msg)
            print(f"✅ Enviada: {msg}")
            time.sleep(0.5)
        producer.flush()
        print("✅ Todas as mensagens foram enviadas com sucesso!\n")
    except KafkaError as e:
        print(f"❌ Erro ao enviar mensagens: {e}")

def testar_consumidor():
    print("🔹 Testando consumo de mensagens do Kafka...")
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="grupo_teste",
            value_deserializer=lambda v: v.decode("utf-8"),
        )
        for msg in consumer:
            print(f"📩 Recebida: {msg.value}")
            break  # sai após receber a primeira mensagem
        consumer.close()
        print("✅ Conexão e leitura bem-sucedidas!")
    except KafkaError as e:
        print(f"❌ Erro ao consumir mensagens: {e}")

if __name__ == "__main__":
    testar_produtor()
    time.sleep(2)
    testar_consumidor()
