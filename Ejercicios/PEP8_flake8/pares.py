def calcular_numeros_pares():
    """
    Calcula los primeros 50 números pares.
    
    Returns:
        list: Lista con los primeros 50 números pares
    """
    numeros_pares = []
    numero = 0
    
    while len(numeros_pares) < 50:
        if numero % 2 == 0:
            numeros_pares.append(numero)
        numero += 1
    
    return numeros_pares


# Ejemplo de uso
if __name__ == "__main__":
    pares = calcular_numeros_pares()
    print("Los primeros 50 números pares son:")
    print(pares)

