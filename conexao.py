from time import sleep

import requests
import json

url = "http://172.28.0.14:8088/query"

payload = json.dumps({
    "ksql": """
SELECT l.*
FROM LINHAS_ONIBUS_RAW l

EMIT CHANGES;



""",
    "streamsProperties": {
        "auto.offset.reset": "earliest"
    }
})

headers = {
    'Content-Type': 'application/vnd.ksql.v1+json'
}

with requests.post(url, headers=headers, data=payload, stream=True) as response:
    for line in response.iter_lines():
        print(line)
        sleep(90)

        if line:
            print(json.loads(line))

        print('=' * 100)

