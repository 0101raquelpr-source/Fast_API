
from fastapi import FastAPI,Body,HTTPException 
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()
app.title = "App Movies"
app.version = "1.0.0"

class Movie(BaseModel):
    id: int
    title: str
    overview: str 
    year: int
    rating: float
    category: str



class MovieCreate(BaseModel): 
    #Validations are created with Field(pydantic)
    id: int
    title: str = Field(min_length=5, max_length=40)
    overview: str  = Field(min_length=15)
    year: int = Field(gt=1900)
    rating: float = Field(gt=0, le=10, default=5)
    category: str = Field(min_length=5, max_length=40, default="No category")

    # set default values ​​in the model
    '''model_config = {"json_schema_extra": {
        "example": {'id':1,
                    'title':"Movie title", 'overview':"Movie overview",
                    'year':2023, 'rating':7.5, 'category':"Category"}}}'''

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    category: Optional[str] = None


movies:list[Movie] = []

@app.get('/', tags=['Home'])
def home():
    return "HoMe"


@app.get('/movies', tags=['Movies'])
def get_all_movies() -> list[Movie]:
    return [movie.model_dump() for movie in movies] 


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id:int) -> Movie:
    for m in movies:
        if m.id == id:
            return m
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category:str, year:int) -> Movie:
    for m in movies:
        if m['category'].lower() == category.lower() and m['year'] == year:
            return m
        raise HTTPException(status_code=404, detail="Movie Category not found")


@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> list[Movie]:
    movies.append(movie)
    return [movie.model_dump() for movie in movies] 

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id:int, movie:MovieUpdate):
    for m in movies:
        if m['id'] == id:
            m['title'] = movie.title
            m['overview'] = movie.overview
            m['year'] = movie.year
            m['rating'] = movie.rating
            m['category'] = movie.category
    return {'message': 'Movie updated'}

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int):
    for m in movies:
        if m['id'] == id:
            movies.remove(m)
            return {'message': 'Movie deleted'}
    return {'message': 'Movie not found'}