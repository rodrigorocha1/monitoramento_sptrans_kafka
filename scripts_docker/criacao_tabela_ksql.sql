https://chatgpt.com/c/692cea9d-a2a8-8325-b1f5-4ec7f090f77c -> padrão de projeto


CREATE STREAM ONIBUS_POSICAO_BRUTO (
    c STRING,
    cl INTEGER,
    sl INTEGER,
    lt0 STRING,
    lt1 STRING,
    qv INTEGER,
    p INTEGER,
    a BOOLEAN,
    ta STRING,
    py DOUBLE,
    px DOUBLE
) WITH (
    KAFKA_TOPIC = 'linhas_onibus',
    VALUE_FORMAT = 'JSON'
);


CREATE TABLE ONIBUS_POSICAO_ATUAL AS
SELECT
    p,
    LATEST_BY_OFFSET(py) AS py,
    LATEST_BY_OFFSET(px) AS px,
    LATEST_BY_OFFSET(ta) AS ta
FROM ONIBUS_POSICAO_BRUTO
GROUP BY p;

CREATE TABLE ONIBUS_POSICAO_ATUAL AS
SELECT
    p,
    LATEST_BY_OFFSET(c) AS c,
    LATEST_BY_OFFSET(py) AS py,
    LATEST_BY_OFFSET(p) AS id_onibus,
    LATEST_BY_OFFSET(px) AS px,
    LATEST_BY_OFFSET(ta) AS ta
FROM ONIBUS_POSICAO_BRUTO
GROUP BY p;
---

CREATE TABLE ONIBUS_POSICAO_ATUAL AS
SELECT
    p, c,
    LATEST_BY_OFFSET(py) AS py,
    LATEST_BY_OFFSET(px) AS px,
    LATEST_BY_OFFSET(ta) AS ta
FROM ONIBUS_POSICAO_BRUTO
GROUP BY p, c;

CREATE TABLE ONIBUS_POSICAO_ATUAL AS
SELECT
    p, LATEST_BY_OFFSET(c) as c,
    LATEST_BY_OFFSET(py) AS py,
    LATEST_BY_OFFSET(px) AS px,
    LATEST_BY_OFFSET(ta) AS ta
FROM ONIBUS_POSICAO_BRUTO
GROUP BY p;



----


CREATE STREAM ONIBUS_POSICAO_REKEY
    WITH (PARTITIONS = 6) AS
SELECT *
FROM ONIBUS_POSICAO_BRUTO
PARTITION BY p;


CREATE STREAM ONIBUS_POSICAO_REKEY_V2 AS
SELECT
    *
FROM ONIBUS_POSICAO_BRUTO
PARTITION BY p;



CREATE STREAM ONIBUS_POSICAO_ANTERIOR_ATUAL AS
SELECT
    s.p,
    t.py AS prev_py,
    t.px AS prev_px,
    t.ta AS prev_ta,
    s.py AS curr_py,
    s.px AS curr_px,
    s.ta AS curr_ta
FROM ONIBUS_POSICAO_REKEY s
LEFT JOIN ONIBUS_POSICAO_ATUAL t
    ON s.p = t.p;




CREATE STREAM ONIBUS_POSICAO_ANTERIOR_ATUAL AS
SELECT
    s.p,
    t.c as c,
    t.py AS prev_py,
    t.px AS prev_px,
    t.ta AS prev_ta,
    s.py AS curr_py,SES
    s.px AS curr_px,
    s.ta AS curr_ta
FROM ONIBUS_POSICAO_REKEY s
LEFT JOIN ONIBUS_POSICAO_ATUAL t
    ON s.p = t.p;

CREATE TABLE ONIBUS_POSICAO_ATUAL_V2 AS
SELECT
    S_P,
    LATEST_BY_OFFSET(prev_py) AS prev_py,
    LATEST_BY_OFFSET(prev_px) AS prev_px,
    LATEST_BY_OFFSET(prev_ta) AS prev_ta,
    LATEST_BY_OFFSET(curr_py) AS curr_py,
    LATEST_BY_OFFSET(curr_px) AS curr_px,
    LATEST_BY_OFFSET(curr_ta) AS curr_ta
FROM ONIBUS_POSICAO_ANTERIOR_ATUAL
GROUP BY p;







SELECT
    S_P,
    C,
    prev_py AS PREV_PY,
    prev_px AS PREV_PX,
    prev_ta AS PREV_TA,
    curr_py AS CURR_PY,
    curr_px AS CURR_PX,
    curr_ta AS CURR_TA,
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
WHERE curr_ta IS NOT NULL AND PREV_PY is not null ;



CREATE TABLE ONIBUS_POSICAO_VELOCIDADE_ATUAL AS
SELECT
    S_P,
    LATEST_BY_OFFSET(prev_py) AS prev_py,
    LATEST_BY_OFFSET(prev_px) AS prev_px,
    LATEST_BY_OFFSET(prev_ta) AS prev_ta,
    LATEST_BY_OFFSET(curr_py) AS curr_py,
    LATEST_BY_OFFSET(curr_px) AS curr_px,
    LATEST_BY_OFFSET(curr_ta) AS curr_ta,
    ROUND(
        velocidade_media(
            CAST(LATEST_BY_OFFSET(prev_py) AS DECIMAL(9,6)),
            CAST(LATEST_BY_OFFSET(prev_px) AS DECIMAL(9,6)),
            CAST(LATEST_BY_OFFSET(curr_py) AS DECIMAL(9,6)),
            CAST(LATEST_BY_OFFSET(curr_px) AS DECIMAL(9,6)),
            CONCAT(LATEST_BY_OFFSET(prev_ta),'Z'),
            CONCAT(LATEST_BY_OFFSET(curr_ta),'Z')
        ), 2
    ) AS VELOCIDADE_KMH
FROM ONIBUS_POSICAO_ANTERIOR_ATUAL
GROUP BY S_P
EMIT CHANGES;



SELECT
    S_P,
    c,
    prev_py AS PREV_PY,
    prev_px AS PREV_PX,
    prev_ta AS PREV_TA,
    curr_py AS CURR_PY,
    curr_px AS CURR_PX,
    curr_ta AS CURR_TA,
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
WHERE curr_ta IS NOT NULL AND PREV_PY is not null ;



SELECT *
FROM ONIBUS_POSICAO
WHERE c = '7002-10'	;



SELECT *
FROM ONIBUS_POSICAO EMIT CHANGES;


CREATE TABLE ONIBUS_C_DISTINCT AS
SELECT
    c,
    LATEST_BY_OFFSET(c) AS c_valida
FROM ONIBUS_POSICAO
GROUP BY c;

SET 'auto.offset.reset' = 'latest';

====================================================
CREATE STREAM ONIBUS_POSICAO_REKEY_V2 AS
SELECT
    CONCAT(c, '-', lt0, '-', lt1) AS chave_distinta,
    c,
    lt0,
    lt1
FROM ONIBUS_POSICAO_BRUTO
PARTITION BY CONCAT(c, '-', lt0, '-', lt1);

CREATE TABLE ONIBUS_C_LT0_LT1_DISTINCT AS
SELECT
    chave_distinta,
    LATEST_BY_OFFSET(c) AS c_valido,
    LATEST_BY_OFFSET(lt0) AS lt0_valido,
    LATEST_BY_OFFSET(lt1) AS lt1_valido
FROM ONIBUS_POSICAO_REKEY
GROUP BY chave_distinta;
===================================================

https://medium.com/@khan_79491/using-udf-in-ksqldb-inside-of-a-container-8360721f624b
Using UDF in KSQLDB inside of a container
Yekaterina Khan
Yekaterina Khan

Follow
4 min read
·
Jul 5, 2024



I work as a data engineer at Kolesa Group. With our DWH team
Aidyn Issatayev
,
Babur Rustauletov
,
Zharkynbek Dindar
 we started deploying streaming in the company. We already had RedPanda running and chose Kafka Connect, Schema
 registry and KsqlDB architecture for streamig data from different sources to Google BigQuery. This services are
  deployed in kubernetes and the whole deploying proccess needs separate article.

Press enter or click to view image in full size

In this flow we use KsqlDB for data transformation. After deploying this three services
 and eventually streaming data from MongoDB to RedPanda we began to notice a lot of
 errors flowing to our KsqlDB log like:

{"type":1,"deserializationError":null,"recordProcessingError":
{"errorMessage":"Error processing DOUBLE","record":null,
"cause":["For input string: \"{\"$numberLong\":\"8255552255\"}\""]},
"productionError":null,"serializationError":null,
"kafkaStreamsThreadError":null}
We could solve this by writing a lot of SQL code using REGEXP, CAST and a lot of CASE WHEN, but using UDF seemed more elegant and challenging because we never used that before. And knowing how to build your own user defined function gives more flexibility. Also we not only can use UDF in KsqlDB but run KsqlDB inside of a container that includes our built function.

Creating UDF jar file with maven
In order to create UDF in KsqlDB you have to have JDK and MAVEN installed. We’ll start with installing maven on linux:

sudo apt update
sudo apt install maven
To check if maven installed run:

mvn -version
Let’s create a folder for maven project and cd into it:

mkdir ksql-udf
cd ksql-udf/
To create maven project run:

mvn archetype:generate -DgroupId=com.company.ksql \
-DartifactId=ksql-udf \
-DarchetypeArtifactId=maven-archetype-quickstart \
-DinteractiveMode=false

After firing this comand ksql-udf (DartifactId=ksql-udf) folder will be created. And inside of
 this folder we will have pom.xml and src folder. We will create UDF inside src/main/java/com/company/ksql,
 com/company/ksql generated from DgroupId parameter.

Our task from problem mentioned above is to create function in ksql that will take number as a String
and sometimes json in form of ‘{\”$numberLong\”:\”5000000000\”}’ and convert it to a number.

In pom.xml all dependencies will be listed for this task, if you have different task you may need additional dependencies:

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.company.ksql</groupId>
  <artifactId>ksql-udf</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>ksql-udf</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
    <!-- ksqlDB dependencies -->
    <dependency>
      <groupId>io.confluent.ksql</groupId>
      <artifactId>ksqldb-udf</artifactId>
      <version>7.0.1</version>
    </dependency>
    <!-- JSON library dependency -->
    <dependency>
      <groupId>org.json</groupId>
      <artifactId>json</artifactId>
      <version>20201115</version>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
        <configuration>
          <source>11</source>
          <target>11</target>
        </configuration>
      </plugin>
    </plugins>
  </build>
  <repositories>
    <repository>
      <id>confluent</id>
      <url>https://packages.confluent.io/maven/</url>
    </repository>
  </repositories>
</project>
Next add UDF java files, that implements our task of converting String to number, to src/main/java/com/company/ksql path:

package com.company.ksql;

import io.confluent.ksql.function.udf.Udf;
import io.confluent.ksql.function.udf.UdfDescription;
import io.confluent.ksql.function.udf.UdfParameter;
import org.json.JSONObject;

@UdfDescription(name = "parseMongoNumber", description = "Parses plain numeric string or json to a plain numeric value")
public class ParseMongoNumberUdf {

    @Udf(description = "Parses plain numeric string or json to a plain numeric value")
    public Double parseMongoNumber(@UdfParameter(value = "input", description = "Input or plain numeric string") final String input) {

        if (input == null || input.isEmpty()) {
            return null; // or return a default value, e.g., 0.0
        }

        // Check if the string is a plain number
        try {
            return Double.parseDouble(input);
        } catch (NumberFormatException e) {
            // Not a plain numeric string, try parsing as JSON
            try {
                JSONObject obj = new JSONObject(input);
                return obj.getDouble("$numberLong");
            } catch (Exception ex) {
                throw new IllegalArgumentException("Input string is not a valid number or MongoDB Extended JSON: " + input, ex);
            }
        }
    }
}
File name should be as class name i.e. ParseMongoNumberUdf.java

Get Yekaterina Khan’s stories in your inbox
Join Medium for free to get updates from this writer.

Enter your email
Subscribe
and package name should corespond to DgroupId and path where java files located.

Go to folder where your pom.xml is located and run:

mvn clean package
After successful run target folder should appear with jar file.

Build image with jar file
Now that we successfully build our ksql-udf-1.0-SNAPSHOT.jar, let’s move it inside of a container.
 Create dockerfile. My dockerfile is located outside of first ksql-udf folder. Our jar file will be
 located in /opt/ksql/ext/ path, that we have to provide when running container:

FROM confluentinc/cp-ksqldb-server:7.6.1

USER root

RUN mkdir -p /opt/ksql/ext/ && chmod -R 777 /opt/ksql/ext/

COPY ksql-udf/ksql-udf/target/ksql-udf-1.0-SNAPSHOT.jar /opt/ksql/ext/

USER appuser
Buld image:

docker build -t ksql-with-udf .
Finally run container:

docker run -d --rm -p8088:8088 \
  --name=my-ksqldb \
  -e KSQL_LISTENERS=http://0.0.0.0:8088 \
  -e KSQL_KSQL_LOGGING_PROCESSING_TOPIC_AUTO_CREATE=true \
  -e KSQL_KSQL_LOGGING_PROCESSING_STREAM_AUTO_CREATE=true \
  -e KSQL_BOOTSTRAP_SERVERS=localhost:9092 \
  -e KSQL_COMPRESSION_TYPE=snappy \
  -e KSQL_KSQL_SCHEMA_REGISTRY_URL=http://localhost:8081 \
  -e KSQL_KSQL_STREAM_PRODUCER_DELIVERY_TIMEOUT_MS=2147483647 \
  -e KSQL_KSQL_STREAM_PRODUCER_MAX_BLOCK_MS=9223372036854775807 \
  -e KSQL_KSQL_INTERNAL_TOPIC_REPLICAS=3 \
  -e KSQL_KSQL_INTERNAL_TOPIC_MIN_INSYNC_REPLICAS=2 \
  -e KSQL_KSQL_STREAMS_REPLICATION_FACTOR=3 \
  -e KSQL_KSQL_STREAMS_PRODUCER_ACKS=all \
  -e KSQL_KSQL_STREAMS_TOPIC_MIN_INSYNC_REPLICAS=2 \
  -e KSQL_KSQL_STREAMS_NUM_STANDBY_REPLICAS=1 \
  -e KSQL_CONFIG_OVERRIDE_POLICY=All \
  -e KSQL_KSQL_SERVICE_ID=ksql-server \
  -e KSQL_KSQL_EXTENSION_DIR="/opt/ksql/ext/" \
  ksql-with-udf
If you have Kafka or Redpanda cluster and Schema regisrty running on server, provide corresponding ip address.

You can check if extension dir set up correctly by running in ksql:

list properties;
and function created:

list functions;
Finally we can use our function:

SELECT parseMongoNumber('{"$numberLong":"8042728000"}') json_format,
parseMongoNumber('8042728000') string_format
FROM your_stream;
======================================================