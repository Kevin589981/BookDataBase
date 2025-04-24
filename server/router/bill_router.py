from fastapi import APIRouter, Depends, HTTPException, Query, status,Response
from sqlalchemy.orm import Session
from typing import Optional
from server.database import get_db
from server.schemas.bill_schemas import PaginatedBillResponse,BillDetail
from server import db_models
from server import auth
from sqlalchemy import desc, asc
from datetime import datetime,date,time
router = APIRouter(prefix="/bills", tags=["bills"])

@router.get("/", 
           response_model=PaginatedBillResponse,
           dependencies=[Depends(auth.Auth.get_current_user)])
def query_bills(
    # 筛选参数
    bill_type: Optional[str] = Query(
        None, 
        regex="^(进货|零售)$",
        description="按账单类型筛选（进货/零售）"
    ),
    start_date: Optional[date] = Query(None, description="开始日期（包含）"),
    end_date: Optional[date] = Query(None, description="结束日期（包含）"),
    min_amount: Optional[float] = Query(None, ge=0, description="最小金额"),
    max_amount: Optional[float] = Query(None, ge=0, description="最大金额"),
    operator_id: Optional[str] = Query(None, description="按操作员工号查询"),
    exact_operator_id: Optional[bool] = Query(False, description="操作员工号精确匹配"),
    related_order: Optional[int] = Query(None, description="关联订单ID"),

    # 排序参数
    sort_by: Optional[str] = Query(
        None, 
        regex="^(transaction_time|amount|bill_type)$",
        description="排序字段（transaction_time/amount/bill_type）"
    ),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    
    # 分页参数
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    
    db: Session = Depends(get_db)
) -> PaginatedBillResponse:
    # 基础查询
    query = db.query(db_models.Bill)

    # 处理日期范围转换（将date转为datetime）
    if start_date:
        start_datetime = datetime.combine(start_date, time.min)
        query = query.filter(db_models.Bill.transaction_time >= start_datetime)
    if end_date:
        end_datetime = datetime.combine(end_date, time.max)
        query = query.filter(db_models.Bill.transaction_time <= end_datetime)

    # 应用其他筛选条件
    if bill_type:
        query = query.filter(db_models.Bill.bill_type == bill_type)
    if min_amount is not None:
        query = query.filter(db_models.Bill.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(db_models.Bill.amount <= max_amount)
    if operator_id:
        if exact_operator_id:
            query = query.filter(db_models.Bill.operator_id == operator_id)
        else:
            query = query.filter(db_models.Bill.operator_id.contains(operator_id))
    if related_order:
        query = query.filter(db_models.Bill.related_order == related_order)

    # 处理排序
    sort_mapping = {
        "transaction_time": db_models.Bill.transaction_time,
        "amount": db_models.Bill.amount,
        "bill_type": db_models.Bill.bill_type
    }
    
    if sort_by:
        order_column = sort_mapping[sort_by]
        order_func = desc if sort_order == "desc" else asc
        query = query.order_by(order_func(order_column))
    else:
        # 默认按交易时间降序
        query = query.order_by(desc(db_models.Bill.transaction_time))

    # 分页处理
    total = query.count()
    bills = query.offset((page - 1) * page_size).limit(page_size).all()

    # 构建响应数据
    items = [
        BillDetail(
            id=bill.id,
            bill_type=bill.bill_type,
            amount=float(bill.amount),
            transaction_time=bill.transaction_time,
            related_order=bill.related_order,
            operator_id=bill.operator_id
        ) for bill in bills
    ]

    return PaginatedBillResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )