from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class SaleItemCreate(BaseModel):
    book_isbn: str
    quantity: int

class PaymentResponse(BaseModel):
    message: str
    order_id: int
    transaction_no: Optional[str] = None
    total_amount: Optional[float] = None

# 销售项目详情
class SaleItemDetail(BaseModel):
    id: int
    book_isbn: str
    book_title: Optional[str] = None
    quantity: int
    sold_price: float
    total_amount: float
    
    class Config:
        from_attributes = True

# 销售订单详情
class SaleOrderDetail(BaseModel):
    id: int
    transaction_no: str
    total_amount: float
    payment_method: Optional[str] = None
    operator_id: str
    operator_name: Optional[str] = None
    created_at: datetime
    items: List[SaleItemDetail] = []
    
    class Config:
        from_attributes = True

# 销售订单列表项
class SaleOrderListItem(BaseModel):
    id: int
    transaction_no: str
    total_amount: float
    payment_method: Optional[str] = None
    operator_id: str
    operator_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# 分页响应
class PaginatedSaleOrderResponse(BaseModel):
    data: List[SaleOrderListItem]
    total: int
    page: int
    page_size: int

# 销售订单查询参数
class SaleOrderQueryParams(BaseModel):
    transaction_no: Optional[str] = None
    payment_method: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    operator_id: Optional[str] = None
    page: int = 1
    page_size: int = 10
    sort_by: str = "created_at"
    sort_order: str = "desc"

# 销售订单更新
class SaleOrderUpdate(BaseModel):
    payment_method: Optional[str] = None
    remark: Optional[str] = None