numeros = [3, 1, 2, 4, 7, 6, 9, 8]

pares = [n for n in numeros if n % 2 == 0]
impares = [n for n in numeros if n % 2 != 0]

resultado = pares + impares

print(resultado)