from sqlmodel import create_engine, Session, SQLModel
from pathlib import Path
from src.models import tables
import os


#  Absolute Path

DB_DIR = Path("/data") #para usar SQLite en un volumen de Docker
if not DB_DIR.exists():
    DB_DIR.mkdir(parents=True, exist_ok=True)

sqlite_file_name = "database_fast_api.db"
db_path = DB_DIR / sqlite_file_name
sqlite_url = f"sqlite:///{db_path}"
# Motor de SQL
engine = create_engine(sqlite_url, echo=True)
'''
#Esta parte es para una bbdd fuera de Docker compose.
BASE_DIR = Path(__file__).resolve().parent
sqlite_file_name = "database.db"
db_path = BASE_DIR / sqlite_file_name
sqlite_url = f"sqlite:///{db_path}"
# Make SQL Motor. `echo=True` prints all sql statements
engine = create_engine(sqlite_url, echo=True)
'''

# This function will make the database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# A Session is the unit of work for all interactions with the database.
def get_session():
    with Session(engine) as session:
        yield session