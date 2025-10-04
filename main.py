
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
def get_movie_by_category(category: Optional[str] = None, year: Optional[int] = None) -> list[Movie]:
    results = [] # Cambiamos para buscar múltiples resultados
    if not category and not year:
        raise HTTPException(status_code=400, detail="Debe especificar al menos 'category' o 'year'")

    for m in movies:
        match = True 
        if category and m.category.lower() != category.lower():
            match = False  
        if year and m.year != year:
            match = False           
        if match:
            results.append(m)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron películas con esos criterios")
    return results 


@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> list[Movie]:
    movies.append(movie)
    return [movie.model_dump() for movie in movies] 

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> Movie:
    update_data = movie.model_dump(exclude_unset=True) 
    for m in movies:
        if m.id == id:
            for key, value in update_data.items():
                setattr(m, key, value)
            
            return m
            
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for m in movies:
        if m.id == id:
            movies.remove(m)
            return {'message': 'Movie Deleted'}
    raise HTTPException(status_code=404, detail="Movie not found")