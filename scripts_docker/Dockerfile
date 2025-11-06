# Usar Java 11 (compatível com Kafka 3.5.x)
FROM eclipse-temurin:11-jre

# Variáveis de ambiente principais
ENV KAFKA_VERSION=3.5.1
ENV SCALA_VERSION=2.13
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$PATH:$KAFKA_HOME/bin

# Instalar dependências e baixar Kafka
RUN apt-get update && apt-get install -y wget tar net-tools iproute2 curl && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -O /tmp/kafka.tgz && \
    mkdir -p /opt/kafka && \
    tar -xzf /tmp/kafka.tgz --strip 1 -C /opt/kafka && \
    rm /tmp/kafka.tgz

# Expor portas padrão
# 2181 -> Zookeeper
# 9092 -> Kafka Broker
EXPOSE 2181 9092

# Copiar script de inicialização
COPY start-kafka-zookeeper.sh /usr/bin/start-kafka-zookeeper.sh
RUN chmod +x /usr/bin/start-kafka-zookeeper.sh

# Comando padrão
CMD ["bash", "/usr/bin/start-kafka-zookeeper.sh"]
