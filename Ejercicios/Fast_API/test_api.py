import requests

BASE_URL = "http://localhost:8000"

def test_api():
    # 1. Crear películas
    movies_to_create = [
        {
            "id": 1,
            "title": "El Padrino",
            "overview": "Una historia clásica de la mafia italiana en Nueva York",
            "year": 1972,
            "rating": 9.2,
            "category": "Drama clásico"
        },
        {
            "id": 2,
            "title": "Pulp Fiction",
            "overview": "Historias entrecruzadas en Los Angeles California",
            "year": 1994,
            "rating": 8.9,
            "category": "Crimen negro"
        },
        {
            "id": 3,
            "title": "El Señor de los Anillos",
            "overview": "Una aventura épica en la Tierra Media con hobbits",
            "year": 2001,
            "rating": 8.8,
            "category": "Fantasía épica"
        },
        {
            "id": 4,
            "title": "Matrix Revoluciones",
            "overview": "Un programador descubre la verdad sobre su mundo",
            "year": 1999,
            "rating": 8.7,
            "category": "Ciencia ficción"
        }
    ]

    try:
        print("1. Creando películas...")
        for movie in movies_to_create:
            response = requests.post(f"{BASE_URL}/movies", json=movie)
            if response.status_code == 200:
                print(f"Película creada: {movie['title']}")
            else:
                print(f"Error al crear {movie['title']}: {response.text}")

        print("\n2. Mostrando todas las películas:")
        response = requests.get(f"{BASE_URL}/movies")
        print(response.json())

        print("\n3. Actualizando categoría de Matrix...")
        update_data = {"category": "Acción futurista"}
        response = requests.put(f"{BASE_URL}/movies/4", json=update_data)
        if response.status_code == 200:
            print("Película actualizada exitosamente")
        else:
            print(f"Error al actualizar: {response.text}")

        print("\n4. Eliminando El Padrino (ID: 1)...")
        response = requests.delete(f"{BASE_URL}/movies/1")
        if response.status_code == 200:
            print("Película eliminada exitosamente")
        else:
            print(f"Error al eliminar: {response.text}")

        print("\n5. Mostrando lista final de películas:")
        response = requests.get(f"{BASE_URL}/movies")
        print(response.json())

    except requests.exceptions.ConnectionError:
        print("Error: No se puede conectar al servidor. Asegúrate de que la API está corriendo.")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    test_api()