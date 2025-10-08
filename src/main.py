
import os
from fastapi import FastAPI,status,Body,HTTPException, Path, Query,Depends
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse,Response,JSONResponse
from src.routers.movie_router import movie_router   
from typing import Union, Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path



app = FastAPI()
app.title = "App Movies"
app.version = "1.0.0"

# Stablish path to templates
BASE_DIR = Path(__file__).parent # root path
static_path = BASE_DIR / "static"
templates_path = BASE_DIR / "templates"
app.mount("/static", StaticFiles(directory=static_path),name="static")
templates = Jinja2Templates(directory=templates_path)


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

# HOME Endpoint
@app.get('/', tags=['Home'])
def home(request : Request):
    return templates.TemplateResponse('index.html', {'request': request,'message': 'Welcome'})


# Declare depends:  for common parameters (using a Class)
class CommonDep:
    def __init__(self,start_date:str, end_date : str) -> None:
        self.start_date = start_date
        self.end_date = end_date


# Using depends
@app.get('/users',tags=['Home'])
def get_users(commons: CommonDep = Depends()):
    return f"Users created betwen {commons.start_date} and {commons.end_date}"

@app.get('/customers',tags=['Home'])
def get_customers(commons: CommonDep = Depends()):
    return f"Customers created between {commons.start_date} and {commons.end_date}"

# Adding other app functions included in ./routers/movie_router.py
app.include_router(prefix='/movies', router = movie_router)
