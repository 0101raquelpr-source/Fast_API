import pytest # type: ignore
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.main import app
from src.database import get_session
from src.models.tables import Movie as MovieDB

client = TestClient(app)

# ----------------------------------------------------------------------
# TEST DATABASE SETUP
# ----------------------------------------------------------------------

@pytest.fixture(name="session")
def session_fixture():
    """
    Creates a temporary in-memory SQLite database for testing.
    This fixture yields a session and handles setup and teardown.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Creates a TestClient that uses the temporary test database.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ----------------------------------------------------------------------
# ENDPOINT TESTS
# ----------------------------------------------------------------------

def test_home_endpoint(client: TestClient):
    """Tests the home ('/') endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Welcome" in response.text

# --- POST ---

def test_create_movie_success(client: TestClient):
    """Tests successful movie creation (POST /movies)."""
    new_movie_data = {
        "title": "New Movie Title Test", 
        "overview": "A detailed overview for the new movie, which is long enough.",
        "year": 2023, 
        "rating": 7.5, 
        "category": "Comedy"
    }
    response = client.post("/movies/", json=new_movie_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == new_movie_data["title"]
    assert data["overview"] == new_movie_data["overview"]
    assert "id" in data
    assert data["id"] is not None

def test_create_movie_validation_error(client: TestClient):
    """Tests creation with invalid data (should fail with 422)."""
    # overview is too short (min_length=15)
    invalid_data = {"title": "Valid Title", "overview": "Too short."}
    response = client.post("/movies/", json=invalid_data)
    assert response.status_code == 422 


# --- GET ALL & GET BY ID ---

def test_get_all_movies(session: Session, client: TestClient):
    """Tests getting all movies (GET /movies)."""
    movie_1 = MovieDB(title="Movie One", overview="Overview for movie one.", year=2021, rating=8, category="Action")
    movie_2 = MovieDB(title="Movie Two", overview="Overview for movie two.", year=2022, rating=7, category="Comedy")
    session.add(movie_1)
    session.add(movie_2)
    session.commit()

    response = client.get("/movies/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Movie One"
    assert data[1]["title"] == "Movie Two"

def test_get_movie_by_id_success(session: Session, client: TestClient):
    """Tests successfully getting a movie by ID (GET /movies/{id})."""
    movie = MovieDB(id=1, title="Specific Movie", overview="Overview here.", year=2020, rating=9, category="Sci-Fi")
    session.add(movie)
    session.commit()

    response = client.get("/movies/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Specific Movie"

def test_get_movie_by_id_not_found(client: TestClient):
    """Tests getting a movie with a non-existent ID (should return 404)."""
    response = client.get("/movies/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"


# --- GET BY CATEGORY ---

def test_get_movie_by_category(session: Session, client: TestClient):
    """Tests searching by category."""
    movie_1 = MovieDB(title="Action Movie", overview="Overview.", year=2021, rating=8, category="Action")
    movie_2 = MovieDB(title="Comedy Movie", overview="Overview.", year=2022, rating=7, category="Comedy")
    session.add(movie_1)
    session.add(movie_2)
    session.commit()

    response = client.get("/movies/by_category?category=action") 
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Action Movie"

# --- PUT ---

def test_update_movie_partial_success(session: Session, client: TestClient):
    """Tests partially updating a movie (PUT /movies/{id})."""
    movie = MovieDB(id=1, title="Original Title", overview="Original overview.", year=2020, rating=8, category="Drama")
    session.add(movie)
    session.commit()

    update_data = {"title": "Title Updated Successfully"}
    response = client.put("/movies/1", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Title Updated Successfully"
    assert data["overview"] == "Original overview." # Should not change


# --- DELETE ---

def test_delete_movie_success(session: Session, client: TestClient):
    """Tests successful movie deletion (DELETE /movies/{id})."""
    movie = MovieDB(id=1, title="To Be Deleted", overview="Overview.", year=2020, rating=5, category="Action")
    session.add(movie)
    session.commit()

    response = client.delete("/movies/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Movie deleted successfully"
    
    # Verify it's gone from the DB
    deleted_movie = session.get(MovieDB, 1)
    assert deleted_movie is None