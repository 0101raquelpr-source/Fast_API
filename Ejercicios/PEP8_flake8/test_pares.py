import unittest
from pares import calcular_numeros_pares

class TestCalcularPares(unittest.TestCase):
    def test_longitud_lista(self):
        """Verifica que la lista tenga exactamente 50 números"""
        resultado = calcular_numeros_pares()
        self.assertEqual(len(resultado), 50)
    
    def test_todos_son_pares(self):
        """Verifica que todos los números en la lista sean pares"""
        resultado = calcular_numeros_pares()
        for numero in resultado:
            self.assertEqual(numero % 2, 0)
    
    def test_orden_correcto(self):
        """Verifica que los números estén en orden ascendente"""
        resultado = calcular_numeros_pares()
        self.assertEqual(resultado, sorted(resultado))
    
    def test_primeros_numeros(self):
        """Verifica que los primeros números sean correctos"""
        resultado = calcular_numeros_pares()
        self.assertEqual(resultado[:5], [0, 2, 4, 6, 8])

if __name__ == '__main__':
    unittest.main()