# test_api.py

import pytest
from fastapi.testclient import TestClient
# IMPORTANTE: Asegúrate de que 'main' es el nombre de tu archivo.
# Asegúrate de importar la app, la lista global, y el modelo Movie.
from main import app, movies, Movie 

# Crea una instancia del cliente de pruebas para simular peticiones
client = TestClient(app)

# ----------------------------------------------------------------------
# FIXTURES (Datos de prueba y utilidades)
# ----------------------------------------------------------------------

# Esto asegura que la lista 'movies' esté limpia y con datos iniciales para cada prueba
@pytest.fixture(autouse=True)
def clean_movies():
    """Limpia y precarga la lista 'movies' con datos que pasan la validación."""
    movies.clear()
    
    # Datos que cumplen las validaciones (longitud mínima, año > 1900, etc.)
    initial_movie_data = {
        "id": 1, 
        "title": "Test Movie 1 Title", 
        "overview": "This is a sufficiently long overview for the test movie number 1.", 
        "year": 2020, 
        "rating": 8.0, 
        "category": "Accion"
    }
    
    # Usa Movie(**data) para crear la instancia del modelo Pydantic
    movies.append(Movie(**initial_movie_data))
    
    # La prueba se ejecuta aquí
    yield

# ----------------------------------------------------------------------
# TESTS POR ENDPOINT
# ----------------------------------------------------------------------

def test_home_endpoint():
    """Prueba el endpoint de inicio ('/')."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "HoMe"

# --- POST ---

def test_create_movie_success():
    """Prueba la creación exitosa de una película (POST /movies)."""
    new_movie_data = {
        "id": 2, 
        "title": "New Movie Title Test", 
        "overview": "A detailed overview for the new movie, which is long enough.",
        "year": 2023, 
        "rating": 7.5, 
        "category": "Comedy"
    }
    response = client.post("/movies", json=new_movie_data)
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Verifica que la película se añadió correctamente al final
    added_movie = response.json()[-1]
    assert added_movie['title'] == "New Movie Title Test"
    assert added_movie['id'] == 2

def test_create_movie_validation_error():
    """Prueba la creación con datos inválidos o faltantes (debería fallar con 422)."""
    # overview es demasiado corto (min_length=15)
    invalid_data = {
        "id": 3, 
        "title": "Short", 
        "overview": "Too short.", 
        "year": 2023,
        "rating": 5.0,
        "category": "Drama"
    }
    response = client.post("/movies", json=invalid_data)
    assert response.status_code == 422 


# --- GET ALL & GET BY ID ---

def test_get_all_movies():
    """Prueba obtener todas las películas (GET /movies)."""
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) == 1 
    # Usamos el título completo del fixture para evitar el error de aserción anterior
    assert response.json()[0]['title'] == "Test Movie 1 Title" 

def test_get_movie_by_id_success():
    """Prueba obtener una película por ID exitosamente (GET /movies/{id})."""
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['category'] == "Accion"

def test_get_movie_by_id_not_found():
    """Prueba obtener una película con ID inexistente (debería dar 404)."""
    response = client.get("/movies/99")
    assert response.status_code == 404
    assert response.json()['detail'] == "Movie not found"


# --- GET BY CATEGORY/YEAR (Con Optional/Opcionales) ---

def test_get_movie_by_category_success_both():
    """Prueba buscar por categoría y año (ambos presentes)."""
    response = client.get("/movies/?category=accion&year=2020") 
    assert response.status_code == 200
    assert response.json()[0]['title'] == "Test Movie 1 Title"

def test_get_movie_by_category_success_only_category():
    """Prueba buscar solo por categoría (year es opcional)."""
    response = client.get("/movies/?category=accion") 
    assert response.status_code == 200
    assert len(response.json()) == 1 

def test_get_movie_by_category_success_only_year():
    """Prueba buscar solo por año (category es opcional)."""
    response = client.get("/movies/?year=2020") 
    assert response.status_code == 200
    assert len(response.json()) == 1 

def test_get_movie_by_category_not_found():
    """Prueba buscar con criterios inexistentes (debería dar 404)."""
    response = client.get("/movies/?category=thriller&year=2020")
    assert response.status_code == 404
    assert response.json()['detail'] == "No se encontraron películas con esos criterios"

def test_get_movie_by_category_no_parameters():
    """Prueba no enviar ningún parámetro (debería dar 400 Bad Request)."""
    response = client.get("/movies/")
    assert response.status_code == 400
    assert response.json()['detail'] == "Debe especificar al menos 'category' o 'year'"


# --- PUT ---

def test_update_movie_partial_success():
    """Prueba actualizar solo el título (PUT /movies/{id})."""
    update_data = {"title": "Title Updated Successfully"}
    response = client.put("/movies/1", json=update_data)
    
    assert response.status_code == 200
    # Verifica que el retorno es el objeto Movie actualizado
    assert response.json()['title'] == "Title Updated Successfully"
    
    # Verifica que el campo NO enviado (overview) NO fue sobrescrito con None
    assert response.json()['overview'] == "This is a sufficiently long overview for the test movie number 1." 

def test_update_movie_not_found():
    """Prueba actualizar una película inexistente (debería dar 404)."""
    update_data = {"title": "Ghost Movie"}
    response = client.put("/movies/99", json=update_data)
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Movie not found"


# --- DELETE ---

def test_delete_movie_success():
    """Prueba la eliminación exitosa de una película (DELETE /movies/{id})."""
    response = client.delete("/movies/1")
    assert response.status_code == 200
    assert response.json()['message'] == "Movie Deleted" # Coincide con tu retorno
    
    # Verifica que la película ya no existe
    check_response = client.get("/movies/1")
    assert check_response.status_code == 404

def test_delete_movie_not_found():
    """Prueba eliminar una película inexistente (debería dar 404)."""
    response = client.delete("/movies/99")
    assert response.status_code == 404
    assert response.json()['detail'] == "Movie not found"