CREATE STREAM ONIBUS_POSICAO (
    c STRING,
    cl BIGINT,
    sl BIGINT,
    lt0 STRING,
    lt1 STRING,
    qv INTEGER,
    p BIGINT,
    a BOOLEAN,
    ta STRING,
    py DOUBLE,
    px DOUBLE
) WITH (
    KAFKA_TOPIC = 'linhas_onibus',
    VALUE_FORMAT = 'JSON'
);

