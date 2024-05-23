from typing import TypeVar, Generic, Sequence
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic import BaseModel, create_model
from math import ceil

T = TypeVar("T")

class CustomParams(BaseModel, AbstractParams):
    current_page: int = 1
    items_per_page: int = 10

    def to_raw_params(self):
        return {
            'limit': self.items_per_page,
            'offset': self.items_per_page * (self.current_page - 1)
        }

class CustomPage(AbstractPage[T], Generic[T]):
    items: Sequence[T]
    current_page: int
    items_per_page: int
    total_items: int
    total_pages: int

    @classmethod
    def create(cls, items: Sequence[T], params: CustomParams, total: int, **kwargs):
        total_pages = ceil(total / params.items_per_page)
        return cls(
            items=items,
            current_page=params.current_page,
            items_per_page=params.items_per_page,
            total_items=total,
            total_pages=total_pages,
            **kwargs
        )