numeros = [1, 2, 4, 5]

for numero in range(numeros[0], numeros[-1] + 1):
    if numero not in numeros:
        print(numero)
        break