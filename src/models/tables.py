from typing import Optional
from sqlmodel import Field, SQLModel # type: ignore

# It will create these tables on SQlite
class Movie(SQLModel, table=True):
    """
    Represents the Movie table in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    overview: str
    year: int
    rating: float
    category: str


class User(SQLModel, table=True):
    """
    Represents the User table in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str  # This will store the hashed password
    role: str  # e.g., "admin", "user"
