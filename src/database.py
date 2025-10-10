from sqlmodel import create_engine, Session, SQLModel
from pathlib import Path
from src.models import tables


#  Absolute Path
BASE_DIR = Path(__file__).resolve().parent
sqlite_file_name = "database.db"
db_path = BASE_DIR / sqlite_file_name
sqlite_url = f"sqlite:///{db_path}"
# Make SQL Motor. `echo=True` prints all sql statements
engine = create_engine(sqlite_url, echo=True)
# This function will make the database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# A Session is the unit of work for all interactions with the database.
def get_session():
    with Session(engine) as session:
        yield session