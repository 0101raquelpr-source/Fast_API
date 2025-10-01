"""
Juego de Piedra, Papel o Tijera.
"""
import random


def determinar_ganador(jugador, computadora):
    """
    Determina el ganador del juego.
    
    Args:
        jugador (str): Elección del jugador
        computadora (str): Elección de la computadora
        
    Returns:
        str: Resultado del juego ('Ganaste!', 'Perdiste!', o 'Empate!')
    """
    if jugador == computadora:
        return "Empate!"
    
    if (jugador == "piedra" and computadora == "tijera") or \
       (jugador == "papel" and computadora == "piedra") or \
       (jugador == "tijera" and computadora == "papel"):
        return "Ganaste!"
    
    return "Perdiste!"


def jugar():
    """
    Función principal para jugar Piedra, Papel o Tijera.
    """
    opciones = ["piedra", "papel", "tijera"]
    
    while True:
        print("\nJuego de Piedra, Papel o Tijera")
        print("Escribe 'salir' para terminar el juego")
        
        # Obtener la elección del jugador
        jugador = input("\nElige piedra, papel o tijera: ").lower()
        
        if jugador == 'salir':
            print("¡Gracias por jugar!")
            break
            
        if jugador not in opciones:
            print("Opción no válida. Por favor, elige piedra, papel o tijera.")
            continue
            
        # Generar elección de la computadora
        computadora = random.choice(opciones)
        
        print(f"\nTú elegiste: {jugador}")
        print(f"La computadora eligió: {computadora}")
        
        # Determinar y mostrar el resultado
        resultado = determinar_ganador(jugador, computadora)
        print(f"\n{resultado}")


if __name__ == "__main__":
    jugar()