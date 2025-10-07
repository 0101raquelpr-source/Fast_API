
from fastapi import FastAPI,Body,HTTPException, Path, Query
from fastapi.responses import PlainTextResponse
from src.routers.movie_router import movie_router   


app = FastAPI()

app.title = "App Movies"
app.version = "1.0.0"

@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content="Welcome to my app with FastAPI", status_code=200)

app.include_router(prefix='/movies', router = movie_router) #adding the router from movie_router.py
