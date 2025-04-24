from typing import List,Optional
from pydantic import BaseModel
from datetime import datetime

class BillDetail(BaseModel):
    id: int
    bill_type: str
    amount: float
    transaction_time: datetime
    related_order: Optional[int]
    operator_id: Optional[str]

class PaginatedBillResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[BillDetail]