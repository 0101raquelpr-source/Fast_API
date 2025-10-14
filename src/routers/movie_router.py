from src.models.movie_model import Movie as MovieResponse, MovieCreate, MovieUpdate
from fastapi import Path, Query, APIRouter, HTTPException, Depends, status
from fastapi.responses import FileResponse, JSONResponse, Response
from src.dependencies import PaginationParams
from src.database import get_session
from sqlmodel import Session, select
from src.models.tables import Movie as MovieDB

movie_router = APIRouter()

@movie_router.get('/get_file', tags=['Files'])
def get_file():
    return FileResponse('files/sample.pdf')

@movie_router.get('/by_category', tags=['Movies'], response_description="Movies filtered by category")
def get_movie_by_category(category:str = Query(min_length=3,max_length=20), session: Session = Depends(get_session)) -> list[MovieResponse]:
    statement = select(MovieDB).where(MovieDB.category.ilike(f"%{category}%"))
    results = session.exec(statement).all()
    if not results: 
        raise HTTPException(status_code=404, detail="Movie Category not found")
    return results

@movie_router.get('/{id}', tags=['Movies'])
def get_movie(id:int = Path(gt=0), session: Session = Depends(get_session)) -> MovieResponse:
    movie = session.get(MovieDB, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@movie_router.get('/', tags=['Movies'], response_description="List all movies")
def get_all_movies(pagination: PaginationParams = Depends(), session: Session = Depends(get_session)) -> list[MovieResponse]:
    statement = select(MovieDB).offset(pagination.offset).limit(pagination.size)
    movies = session.exec(statement).all()
    return movies

@movie_router.post('/', tags=['Movies'], response_model=MovieResponse, status_code=status.HTTP_201_CREATED, response_description="Add a movie")
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)) -> MovieResponse:
    # Convert the Pydantic input model to a dictionary
    movie_data = movie.model_dump()
    new_movie = MovieDB(**movie_data)
    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)
    return new_movie

@movie_router.put('/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate, session: Session = Depends(get_session)) -> MovieResponse:
    db_movie = session.get(MovieDB, id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie_data = movie.model_dump(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(db_movie, key, value)
    
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    
    return db_movie

@movie_router.delete('/{id}', tags=['Movies'], status_code=status.HTTP_200_OK)
def delete_movie(id: int, session: Session = Depends(get_session)) -> dict:
    movie = session.get(MovieDB, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    session.delete(movie)
    session.commit()
    return {"message": "Movie deleted successfully"}