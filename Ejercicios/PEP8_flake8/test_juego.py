"""
Pruebas unitarias para el juego de Piedra, Papel o Tijera.
"""
import unittest
from juego import determinar_ganador


class TestJuego(unittest.TestCase):
    def test_empates(self):
        """Prueba todos los casos de empate."""
        self.assertEqual(determinar_ganador("piedra", "piedra"), "Empate!")
        self.assertEqual(determinar_ganador("papel", "papel"), "Empate!")
        self.assertEqual(determinar_ganador("tijera", "tijera"), "Empate!")
    
    def test_gana_jugador(self):
        """Prueba todos los casos donde gana el jugador."""
        self.assertEqual(determinar_ganador("piedra", "tijera"), "Ganaste!")
        self.assertEqual(determinar_ganador("papel", "piedra"), "Ganaste!")
        self.assertEqual(determinar_ganador("tijera", "papel"), "Ganaste!")
    
    def test_gana_computadora(self):
        """Prueba todos los casos donde gana la computadora."""
        self.assertEqual(determinar_ganador("piedra", "papel"), "Perdiste!")
        self.assertEqual(determinar_ganador("papel", "tijera"), "Perdiste!")
        self.assertEqual(determinar_ganador("tijera", "piedra"), "Perdiste!")


if __name__ == '__main__':
    unittest.main()