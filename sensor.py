lista = [
    {"c": "5164-21", "cl": 1616},
    {"c": "5164-21", "cl": 1616},
    {"c": "5030-10", "cl": 141},
]

unicos = list(
    map(
        dict,
        {frozenset(d.items()) for d in lista}
    )
)

print(unicos)