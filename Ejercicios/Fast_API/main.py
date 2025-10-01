from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from movies import movies_dict as movies
from pydantic import BaseModel, Field
from typing import Optional

#  uvicorn main:app --port 5000 --reload  # comando para correr el servidor
app = FastAPI()
#configuraciones de la app, cuando se accede a /docs
app.title = "FastAPI Title"   
app.version = "0.0.1"

class Movie(BaseModel):
    id: int
    title: str
    overview: str 
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel): 
    #se crean las validaciones con Field (pydantic)
    id: int
    title: str = Field(min_length=5, max_length=40)
    overview: str  = Field(min_length=15, max_length=60)
    year: int = Field(gt=1900, lt=2025)
    rating: float = Field(gt=0, lt=10)
    category: str = Field(min_length=5, max_length=40, default="No category")

    # establecer valores por defecto en el modelo
    model_config = {"json_schema_extra": {
        "example": {'id':1,
                    'title':"Movie title", 'overview':"Movie overview",
                    'year':2023, 'rating':7.5, 'category':"Category"}}}

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    category: Optional[str] = None


@app.get("/", tags=["Home"])
def home(): 
    return {"message": "Api de peliculas"}

@app.get("/movies", tags=["Movies"])
def get_all_movies() -> list[Movie]: 
    return movies   

@app.post("/movies", tags=["Movies"])
def create_movie(movie: Movie) -> list[Movie]:
    movies.append(movie.model_dump())
    return movies

@app.put("/movies", tags=["Movies"])
def update_movie(id: int, movie: MovieUpdate) -> list[Movie]:
    for m in movies:
        if m["id"] == movie.id:
            m["title"] = movie.title
            m["overview"] = movie.overview
            m["year"] = movie.year
            m["rating"] = movie.rating
            m["category"] = movie.category
            return m
    return {"error": "Movie not found"}

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> list[Movie]:
    for index, movie in enumerate(movies):
        if movie["id"] == id:
            movies.pop(index)
            return movies
    return {"error": "Movie not found"}


@app.get("/movies/{id}", tags=["Movies"])
def get_movies(id: int) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return movie
    return  []

@app.get("/movies/", tags=["Movies"])
def get_movie_by_category(category: str, year: int) -> Movie:
    for movie in movies:
        if movie["category"] == category and movie["year"] == year :
            return movie
    return []

