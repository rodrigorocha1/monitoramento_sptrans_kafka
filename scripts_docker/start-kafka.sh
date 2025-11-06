# Usando Java 11 (recomendado para Kafka 3.5.1)
FROM eclipse-temurin:11-jre

# Variáveis de ambiente principais
ENV KAFKA_VERSION=3.5.1
ENV SCALA_VERSION=2.13
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$PATH:$KAFKA_HOME/bin

# Instala dependências necessárias
RUN apt-get update && apt-get install -y wget tar net-tools iproute2 curl && \
    rm -rf /var/lib/apt/lists/*

# Baixa e instala o Apache Kafka
RUN wget https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -O /tmp/kafka.tgz && \
    mkdir -p ${KAFKA_HOME} && \
    tar -xzf /tmp/kafka.tgz --strip 1 -C ${KAFKA_HOME} && \
    rm /tmp/kafka.tgz

# Define variáveis de ambiente padrão
ENV KAFKA_BROKER_ID=1
ENV KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
ENV KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
ENV KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092
ENV KAFKA_LOG_DIRS=/tmp/kafka-logs
ENV ZOOKEEPER_DATA_DIR=/tmp/zookeeper

# Expondo portas do Kafka e Zookeeper
EXPOSE 9092 2181

# Cria script de inicialização
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🔹 Iniciando Zookeeper..."\n\
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &\n\
sleep 5\n\
echo "🔹 Iniciando Kafka Broker..."\n\
exec $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties\n' > /start.sh && \
    chmod +x /start.sh

# Usa a forma JSON recomendada (elimina o warning)
CMD ["bash", "/start.sh"]
