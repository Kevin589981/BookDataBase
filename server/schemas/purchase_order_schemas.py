from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import List
class BookCreateInfo(BaseModel):
    title: str
    author: Optional[str]=None
    publisher: Optional[str]=None
    retail_price: Optional[float]=None

class PurchaseCreateRequest(BaseModel):
    isbn: str
    quantity: int
    purchase_price: float
    book_info: Optional[BookCreateInfo] = None

class PurchaseOrderResponse(BaseModel):
    id: int
    book_isbn: str
    quantity: int
    purchase_price: float
    total_amount: float
    order_date: datetime
    payment_status: str

class PurchaseOrderDetail(BaseModel):
    id: int
    book_isbn: str
    purchase_price: float
    quantity: int
    total_amount: float
    order_date: datetime
    payment_status: str
    operator_id: str
    operator_id2: Optional[str]=None
    operator_id3: Optional[str]=None

class PaginatedPurchaseResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[PurchaseOrderDetail]

class PaymentResponse(BaseModel):
    message: str
    order_id: int
    paid_amount: float

class ReturnResponse(BaseModel):
    message: str
    order_id: int