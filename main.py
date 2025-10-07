
from fastapi import FastAPI,Body,HTTPException, Path, Query
from fastapi.responses import HTMLResponse,PlainTextResponse, RedirectResponse, FileResponse,JSONResponse
from pydantic import BaseModel, Field, field_validator,model_validator
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
    title: str = Field(min_length=2, max_length=60)
    overview: str  = Field(min_length=15)
    year: int = Field(gt=1900)
    rating: float = Field(gt=0, le=10, default=5)
    category: str = Field(min_length=5, max_length=40, default="No category")

    # set default values ​​in the model
    '''model_config = {"json_schema_extra": {
        "example": {'id':1,
                    'title':"Movie title", 'overview':"Movie overview",
                    'year':2023, 'rating':7.5, 'category':"Category"}}}'''
    @model_validator(mode='after')
    def title_must_be_different_from_overview(self) -> 'MovieCreate': 
        if self.title == self.overview:
            raise ValueError('The title cannot be identical to the synopsis (overview).')
        return self

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    category: Optional[str] = None


movies:list[Movie] = []

@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content="Welcome to my app with FastAPI", status_code=200)


@app.get('/movies', tags=['Movies'], response_description="List all movies")
def get_all_movies() -> list[Movie]:
    content = [movie.model_dump() for movie in movies] 
    return JSONResponse(content=content, status_code=200)


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id:int = Path(gt=0)) -> Movie:
    for m in movies:
        if m.id == id:
            return m
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get('/movies/', tags=['Movies'], response_description="Movies filtered by category")
def get_movie_by_category(category:str = Query(min_length=3,max_length=20)) -> list[dict]:
    search_term = category.lower()
    results = [
        m.model_dump() 
        for m in movies 
        if search_term in m.category.lower()
    ]
    if not results: 
        raise HTTPException(status_code=404, detail="Movie Category not found")
    return results
    


@app.post('/movies', tags=['Movies'],response_description="Add a movie")
def create_movie(movie: MovieCreate) -> list[Movie]:
    movies.append(movie)
    #return [movie.model_dump() for movie in movies] 
    return RedirectResponse(url='/movies', status_code=303) #get all movies

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id:int, movie:MovieUpdate):
    for m in movies:
        if m.id == id:
            m.title= movie.title
            m.overview = movie.overview
            m.year = movie.year
            m.rating = movie.rating
            m.category = movie.category
        return {'message': 'Movie updated'}
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int):
    for m in movies:
        if m.id == id:
            movies.remove(m)
            return {'message': 'Movie deleted'}
    raise HTTPException(status_code=404, detail="Movie not found")

@app.get('/get_file', tags=['Files'])
def get_file():
    return FileResponse('files/sample.pdf')