numeros = [1, 2, 4, 5]

# - 1 se refere ao ultimo item da lista.
# o + 1 é para garantir que o último item esteja incluso na comparação.
for numero in range(numeros[0], numeros[-1] + 1):
    if numero not in numeros:
        print(numero)
        break 