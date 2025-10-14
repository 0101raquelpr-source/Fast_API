from __future__ import annotations
from pydantic import BaseModel, Field, model_validator

# Pydantic models for API data structures.
class Movie(BaseModel):
    id: int
    title: str
    overview: str 
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel): 
    title: str = Field(min_length=2, max_length=60)
    overview: str  = Field(min_length=15)
    year: int = Field(gt=1900)
    rating: float = Field(gt=0, le=10, default=5)
    category: str = Field(min_length=5, max_length=40, default="No category")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "My Awesome Movie",
                    "overview": "This is a great movie about an adventure.",
                    "year": 2024,
                    "rating": 8.5,
                    "category": "Adventure"
                }
            ]
        }
    }
    @model_validator(mode='after')
    def title_must_be_different_from_overview(self) -> MovieCreate:
        if self.title == self.overview:
            raise ValueError('The title cannot be identical to the synopsis (overview).')
        return self

class MovieUpdate(BaseModel):
    title: str | None = None
    overview: str | None = None
    year: int | None = None
    rating: float | None = None
    category: str | None = None