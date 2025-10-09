
from src.models.movie_model import Movie, MovieCreate, MovieUpdate
from fastapi import Path, Query, APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, HTMLResponse
from src.dependencies import PaginationParams
from src.database import movies

movie_router = APIRouter()

@movie_router.get('/get_file', tags=['Files'])
def get_file():
    return FileResponse('files/sample.pdf')

@movie_router.get('/by_category', tags=['Movies'], response_description="Movies filtered by category")
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

@movie_router.get('/{id}', tags=['Movies'])
def get_movie(id:int = Path(gt=0)) -> Movie:
    for m in movies:
        if m.id == id:
            return m
    raise HTTPException(status_code=404, detail="Movie not found")

@movie_router.get('/', tags=['Movies'], response_description="List all movies")
def get_all_movies(pagination: PaginationParams = Depends()) -> list[Movie]:
    paginated_movies = movies[pagination.offset : pagination.offset + pagination.size]
    return paginated_movies

@movie_router.post('/', tags=['Movies'],response_description="Add a movie")
def create_movie(movie: MovieCreate) -> list[Movie]:
    movies.append(movie)
    #return [movie.model_dump() for movie in movies] 
    return RedirectResponse(url='/movies', status_code=303) #get all movies

@movie_router.put('/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> Movie:
    update_data = movie.model_dump(exclude_unset=True) 
    for i, m in enumerate(movies):
        if m.id == id:
            updated_movie = m.model_copy(update=update_data)
            movies[i] = updated_movie
            
            return updated_movie 
            
    raise HTTPException(status_code=404, detail="Movie not found")

@movie_router.delete('/{id}', tags=['Movies'])
def delete_movie(id: int):
    for m in movies:
        if m.id == id:
            movies.remove(m)
            return {'message': 'Movie deleted'}
    raise HTTPException(status_code=404, detail="Movie not found")
