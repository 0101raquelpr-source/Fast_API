from fastapi import Query
from typing import Annotated

class PaginationParams:
    """
    Dependency to handle pagination parameters.
    Automatically calculates the offset for database queries.
    """
    def __init__(
        self,
        page: Annotated[int, Query(gt=0, description="Number of page from 1")] = 1,
        size: Annotated[int, Query(gt=0, le=100, description="Number of items per page")] = 10,
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size