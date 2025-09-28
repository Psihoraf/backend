from fastapi import Depends,Query
from pydantic import BaseModel
from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[ int | None, Query(1, ge=1)]
    per_page: Annotated[ int | None , Query(3, ge=0, lt=30)]

PginationDep = Annotated[ PaginationParams, Depends()]