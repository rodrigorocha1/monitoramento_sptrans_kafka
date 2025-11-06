#!/bin/bash
set -e

# Iniciar Zookeeper em background
echo "🦓 Iniciando Zookeeper..."
$KAFKA_HOME/bin/zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties

# Aguardar inicialização do Zookeeper
sleep 5

# Ajustar listeners e host se necessário
echo "⚙️ Configurando Kafka..."
export KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
export KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092

# Iniciar Kafka
echo "🚀 Iniciando Kafka..."
exec $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
