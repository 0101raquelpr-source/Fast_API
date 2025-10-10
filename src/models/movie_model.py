
from typing import Optional
from pydantic import BaseModel, Field, model_validator

# models for treating movies as object classes in code.
class Movie(BaseModel):
    id: int
    title: str
    overview: str 
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel): 
    #Validations are created with Field(pydantic)
    id: int
    title: str = Field(min_length=2, max_length=60)
    overview: str  = Field(min_length=15)
    year: int = Field(gt=1900)
    rating: float = Field(gt=0, le=10, default=5)
    category: str = Field(min_length=5, max_length=40, default="No category")

    # set default values ​​in the model
    '''model_config = {"json_schema_extra": {
        "example": {'id':1,
                    'title':"Movie title", 'overview':"Movie overview",
                    'year':2023, 'rating':7.5, 'category':"Category"}}}'''
    @model_validator(mode='after')
    def title_must_be_different_from_overview(self) -> 'MovieCreate': 
        if self.title == self.overview:
            raise ValueError('The title cannot be identical to the synopsis (overview).')
        return self

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    category: Optional[str] = None