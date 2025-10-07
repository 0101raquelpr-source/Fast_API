
from fastapi import FastAPI,status,Body,HTTPException, Path, Query
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse,Response,JSONResponse
from src.routers.movie_router import movie_router   
from typing import Union 


app = FastAPI()
app.title = "App Movies"
app.version = "1.0.0"

# Middleware 
@app.middleware(middleware_type="http")
async def http_error_handler(request: Request, call_next) -> Union[Response, JSONResponse]:
    try:
        return await call_next(request)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content="Welcome to my app with FastAPI", status_code=200)

app.include_router(prefix='/movies', router = movie_router) #adding the router from movie_router.py
