

from fastapi import FastAPI,status,HTTPException, Depends
from fastapi.requests import Request
from fastapi.responses import Response,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routers.movie_router import movie_router
from src.routers.auth_router import auth_router
from typing import Union
from pathlib import Path
from contextlib import asynccontextmanager
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Startup: Creating database and tables...")
    create_db_and_tables()
    yield
    # Code to run on shutdown (if any)
    print("Shutdown: Application closing.")


app = FastAPI(lifespan=lifespan)
app.title = "App Movies"
app.version = "1.0.0"

# Stablish path to templates
BASE_DIR = Path(__file__).parent # root path
static_path = BASE_DIR / "static"
templates_path = BASE_DIR / "templates"
app.mount("/static", StaticFiles(directory=static_path),name="static")
templates = Jinja2Templates(directory=templates_path)


###  Middleware  ###
@app.middleware(middleware_type="http")
async def http_error_handler(request: Request, call_next) -> Union[Response, JSONResponse]:
    try:
        return await call_next(request)
    except HTTPException as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    except Exception as e:
        # Error 500 
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Unexpected internal server error: {str(e)}"}
        )

# HOME Endpoint
@app.get('/', tags=['Home'])
def home(request : Request):
    response = templates.TemplateResponse('index.html', {'request': request,'message': 'Welcome'})
    response.set_cookie(key="last_visit", value="welcome_user", expires=60)
    return response

# Adding other app functions included in ./routers/movie_router.py and .auth_router 
app.include_router(prefix='/movies', router=movie_router)
app.include_router(prefix='/auth', router=auth_router)
