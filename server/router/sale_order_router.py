from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import random
import string
from server.schemas.sale_order_schemas import (
    SaleItemCreate, PaymentResponse, SaleOrderDetail, 
    SaleOrderListItem, PaginatedSaleOrderResponse, SaleOrderUpdate
)
from server import db_models
from server.database import get_db
from server import auth
from sqlalchemy import desc, asc, and_

router = APIRouter(tags=["sale"],prefix="/sale")

@router.post("/", response_model=PaymentResponse)
def create_sale_order(
    items: List[SaleItemCreate],  
    payment_method: Optional[str] = Query(None, description="支付方式"),
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
):
    """
    创建销售订单并减少库存
    """
    # 生成交易流水号
    transaction_no = generate_transaction_no()
    
    # 计算总金额并验证库存
    total_amount = 0
    sale_items = []
    
    for item in items:
        # 查询书籍信息
        book = db.query(db_models.Book).filter_by(isbn=item.book_isbn).first()
        if not book:
            raise HTTPException(status_code=404, detail=f"ISBN为{item.book_isbn}的书籍不存在")
        
        # 检查库存
        if book.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"书籍《{book.title}》库存不足，当前库存: {book.stock}"
            )
        
        # 检查零售价
        if not book.retail_price:
            raise HTTPException(
                status_code=400,
                detail=f"书籍《{book.title}》未设置零售价"
            )
        
        # 计算单项金额
        item_amount = book.retail_price * item.quantity
        total_amount += item_amount
        
        # 减少库存
        book.stock -= item.quantity
        
        # 创建销售项
        sale_item = db_models.SaleItem(
            book_isbn=item.book_isbn,
            quantity=item.quantity,
            sold_price=book.retail_price,## 没有命名为零售价，可能会有折扣（暂未实现）
            total_amount=item_amount, 
            
        )
        sale_items.append(sale_item)
    
    # 创建销售订单
    sale_order = db_models.SaleOrder(
        transaction_no=transaction_no,
        total_amount=total_amount,
        payment_method=payment_method,
        operator_id=current_user.employee_id,
        sold_items=sale_items
    )
    
    
    try:
        db.add(sale_order)
        db.flush()
        # 创建账单（添加当前时间）
        bill = db_models.Bill(
            bill_type="零售",
            amount=sale_order.total_amount,
            related_order=sale_order.id,
            operator_id=current_user.employee_id,
            transaction_time=datetime.now()
        )
        db.add(bill)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"销售失败: {str(e)}"
        )
    
    return {
        "message": "销售成功",
        "order_id": sale_order.id,
        "transaction_no": sale_order.transaction_no,
        "total_amount": sale_order.total_amount
    }

def parse_date_from_transaction_no(transaction_no):
    """从交易流水号解析日期"""
    if not transaction_no or not transaction_no.startswith("SO") or len(transaction_no) < 16:
        return None
    
    try:
        # 交易流水号格式: SO + 年月日时分秒 + 随机数
        date_part = transaction_no[2:10]  # 提取年月日部分
        year = int(date_part[:4])
        month = int(date_part[4:6])
        day = int(date_part[6:8])
        return datetime(year, month, day)
    except (ValueError, IndexError):
        return None

@router.get("/", response_model=PaginatedSaleOrderResponse)
def get_all_sale_orders(
    # 筛选参数
    transaction_no: Optional[str] = Query(None, description="按交易流水号搜索"),
    exact_transaction_no: Optional[bool] = Query(False, description="交易流水号精确匹配"),
    payment_method: Optional[str] = Query(None, description="按支付方式筛选"),
    operator_id: Optional[str] = Query(None, description="按操作员工号搜索"),
    exact_operator_id: Optional[bool] = Query(False, description="操作员工号精确匹配"),
    min_amount: Optional[float] = Query(None, ge=0, description="最小金额"),
    max_amount: Optional[float] = Query(None, ge=0, description="最大金额"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    
    # 排序参数
    sort_by: Optional[str] = Query("created_at", description="排序字段（created_at/transaction_no/total_amount）"),
    sort_order: Optional[str] = Query("desc", description="排序方向（asc/desc）"),
    
    # 分页参数
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
):
    """
    获取所有销售订单
    """
    # 基础查询
    query = db.query(db_models.SaleOrder)
    
    # 应用筛选条件
    if transaction_no and transaction_no!='':
        if exact_transaction_no:
            query = query.filter(db_models.SaleOrder.transaction_no == transaction_no)
        else:
            query = query.filter(db_models.SaleOrder.transaction_no.contains(transaction_no))
    
    if payment_method:
        query = query.filter(db_models.SaleOrder.payment_method == payment_method)
    
    if operator_id and operator_id!="":
        if exact_operator_id:
            query = query.filter(db_models.SaleOrder.operator_id == operator_id)
        else:
            query = query.filter(db_models.SaleOrder.operator_id.contains(operator_id))
    
    if min_amount is not None:
        query = query.filter(db_models.SaleOrder.total_amount >= min_amount)
    
    if max_amount is not None:
        query = query.filter(db_models.SaleOrder.total_amount <= max_amount)
    
    if start_date:
        query = query.filter(db_models.SaleOrder.created_at >= start_date)
    
    if end_date:
        query = query.filter(db_models.SaleOrder.created_at <= end_date)
    
    # 应用排序
    sort_column = None
    if sort_by == "created_at":
        sort_column = db_models.SaleOrder.created_at
    elif sort_by == "transaction_no":
        sort_column = db_models.SaleOrder.transaction_no
    elif sort_by == "total_amount":
        sort_column = db_models.SaleOrder.total_amount
    else:
        sort_column = db_models.SaleOrder.created_at
    
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    
    # 计算总数
    total = query.count()
    
    # 分页
    orders = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 构建响应
    items = []
    for order in orders:
        # 获取操作员信息
        operator = db.query(db_models.User).filter_by(employee_id=order.operator_id).first()
        operator_name = operator.true_name if operator else None
        
        items.append(
            SaleOrderListItem(
                id=order.id,
                transaction_no=order.transaction_no,
                created_at=order.created_at,
                total_amount=float(order.total_amount),
                payment_method=order.payment_method,
                operator_id=order.operator_id,
                operator_name=operator_name
            )
        )
    # with open(r"D:\Projects\DataBase\debug.txt","w") as f:
    #     f.write(f"\n123{[SaleOrderListItem.from_orm(order) for order in orders]}\n")
    #     f.flush()
    
    return PaginatedSaleOrderResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=items
    )

@router.get("/{order_id}", response_model=SaleOrderDetail)
def get_sale_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
):
    """
    获取销售订单详情
    """
    # 查询订单
    order = db.query(db_models.SaleOrder).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"订单ID {order_id} 不存在")
    
    # 查询操作员姓名
    operator = db.query(db_models.User).filter_by(employee_id=order.operator_id).first()
    operator_name = operator.true_name if operator else None
    
    # 查询订单项
    items = []
    for item in order.sold_items:
        # 查询书籍信息
        book = db.query(db_models.Book).filter_by(isbn=item.book_isbn).first()
        book_title = book.title if book else None
        
        item_data = {
            "id": item.id,
            "book_isbn": item.book_isbn,
            "book_title": book_title,
            "quantity": item.quantity,
            "sold_price": item.sold_price,
            "total_amount": item.total_amount
        }
        items.append(item_data)
    
    # 构建响应
    result = {
        "id": order.id,
        "transaction_no": order.transaction_no,
        "total_amount": order.total_amount,
        "payment_method": order.payment_method,
        "operator_id": order.operator_id,
        "operator_name": operator_name,
        "created_at": order.created_at,
        "items": items
    }
    
    return result

@router.put("/{order_id}", response_model=SaleOrderDetail)
def update_sale_order(
    order_id: int,
    order_update: SaleOrderUpdate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
):
    """
    更新销售订单信息（仅支持更新支付方式和备注）
    """
    # 查询订单
    order = db.query(db_models.SaleOrder).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"订单ID {order_id} 不存在")
    
    # 更新订单信息
    if order_update.payment_method is not None:
        order.payment_method = order_update.payment_method
    
    if order_update.remark is not None:
        order.remark = order_update.remark
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新订单失败: {str(e)}")
    
    # 返回更新后的订单详情
    return get_sale_order_detail(order_id, db, current_user)

@router.delete("/{order_id}")
def delete_sale_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
):
    """
    删除销售订单（软删除，标记为已删除）
    """
    # 查询订单
    order = db.query(db_models.SaleOrder).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"订单ID {order_id} 不存在")
    
    # 检查是否有关联的账单
    bill = db.query(db_models.Bill).filter_by(related_order=order_id).first()
    if bill:
        raise HTTPException(
            status_code=400, 
            detail="该订单已有关联账单，无法删除。如需取消，请创建退货单。"
        )
    
    try:
        # 恢复库存
        for item in order.sold_items:
            book = db.query(db_models.Book).filter_by(isbn=item.book_isbn).first()
            if book:
                book.stock += item.quantity
        
        # 删除订单项
        for item in order.sold_items:
            db.delete(item)
        
        # 删除订单
        db.delete(order)
        db.commit()
        
        return {"message": f"订单ID {order_id} 已成功删除"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除订单失败: {str(e)}")

def generate_transaction_no():
    """生成交易流水号"""
    now = datetime.now()
    date_str = now.strftime("%Y%m%d%H%M%S")
    rand_str = ''.join(random.choices(string.digits, k=6))
    return f"SO{date_str}{rand_str}"