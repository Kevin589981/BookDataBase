from typing import List, Optional
from pydantic import BaseModel, Field

class BookBase(BaseModel):
    isbn: str = Field(..., 
                    min_length=13, 
                    max_length=13, 
                    pattern="^[0-9]*$",
                    example="9787111633333")
    title: str = Field(..., 
                     max_length=100,
                     example="Python编程从入门到实践")
    author: Optional[str] = Field(None,
                                max_length=50,
                                example="Eric Matthes")
    publisher: Optional[str] = Field(None,
                                   max_length=100,
                                   example="人民邮电出版社")
    retail_price: Optional[float] = Field(None,
                              gt=0,
                              example=89.0)
    stock: int = Field(0,
                     ge=0,
                     example=10)

class BookResponse(BookBase):
    class Config:
        from_attributes = True

class BookUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    author: Optional[str] = Field(None, max_length=50)
    publisher: Optional[str] = Field(None, max_length=100)
    retail_price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

class PaginatedBookResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[BookResponse]