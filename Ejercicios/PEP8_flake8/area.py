# area.py

def area_rectangulo(base:float, altura:float) -> float:
    resultado = base * altura
    print(f"El área del rectángulo es: {resultado}")
    return resultado

print(area_rectangulo(5, 3))       # correcto
#print(area_rectangulo("5", "3"))   # error lógico, pero Python lo permite


#   Función que analiza una lista de emails y devuelve únicamente los que son . Mediante regex es como se validarán
import re 
"""
import requests

def obtener_pokemon(nombre: str) -> dict:
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        return {"error": "Pokémon no encontrado"}

# Ejemplo de uso:
print(obtener_pokemon("pikachu"))"""