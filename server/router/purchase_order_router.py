from fastapi import APIRouter, Depends, HTTPException, Query, status,Response
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from server.database import get_db
from server.schemas.purchase_order_schemas import PurchaseOrderResponse,\
    PurchaseCreateRequest,PaymentResponse,ReturnResponse,PaginatedPurchaseResponse,\
        PurchaseOrderDetail
from server import db_models
from server import auth
from datetime import date
from sqlalchemy import desc, asc
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["Purchase Management"],prefix="/purchase")

@router.post("/create_order/", response_model=PurchaseOrderResponse)
def create_purchase_order(
    purchase_data: PurchaseCreateRequest,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
)->PurchaseOrderResponse:
    # 验证ISBN格式
    if len(purchase_data.isbn) != 13 or not purchase_data.isbn.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的ISBN格式（需要13位数字）"
        )
    
    # 检查书籍是否存在
    book = db.query(db_models.Book).filter_by(isbn=purchase_data.isbn).first()
    if not book:
        if not purchase_data.book_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ISBN不存在，必须提供书籍信息"
            )
        # 创建新书
        new_book = db_models.Book(
            isbn=purchase_data.isbn,
            title=purchase_data.book_info.title,
            
            # retail_price=purchase_data.book_info.retail_price,
            stock=0
        )
        
        update_dict = purchase_data.book_info.dict(exclude_unset=True, exclude={"title"})
        for key, value in update_dict.items():
            if value is not None:
                setattr(new_book, key, value)

        try:
            db.add(new_book)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="书籍创建失败，ISBN可能已存在"
            )
    
    # 创建进货订单
    total_amount = purchase_data.quantity * purchase_data.purchase_price
    purchase_order = db_models.PurchaseOrder(
        book_isbn=purchase_data.isbn,
        quantity=purchase_data.quantity,
        purchase_price=purchase_data.purchase_price,
        total_amount=total_amount,
        operator_id=current_user.employee_id
    )
    try:
        db.add(purchase_order)
        db.commit()
        db.refresh(purchase_order)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建订单失败: {str(e)}"
        )
    
    return purchase_order


@router.get("/orders", 
           response_model=PaginatedPurchaseResponse,
           dependencies=[Depends(auth.Auth.get_current_user)])
def query_purchase_orders(
    # 筛选参数
    order_id: Optional[int] = Query(None, description="按订单ID精确查询"),
    book_isbn: Optional[str] = Query(None, description="按ISBN查询"),
    exact_isbn: Optional[bool] = Query(False, description="ISBN精确匹配"),
    payment_status: Optional[str] = Query(None, regex="^(未付款|已付款|已退货|已到货)$", description="按付款状态筛选"),
    operator_id: Optional[str] = Query(None, description="按操作员工号查询"),
    exact_operator_id: Optional[bool] = Query(False, description="操作员工号精确匹配"),
    operator_id2: Optional[str] = Query(None, description="按付款/退货操作员查询"),
    exact_operator_id2: Optional[bool] = Query(False, description="付款/退货操作员工号精确匹配"),
    operator_id3: Optional[str] = Query(None, description="按到货操作员查询"),
    exact_operator_id3: Optional[bool] = Query(False, description="到货操作员工号精确匹配"),
    start_date: Optional[date] = Query(None, description="订单开始日期（包含）"),
    end_date: Optional[date] = Query(None, description="订单结束日期（包含）"),
    min_price: Optional[float] = Query(None, ge=0, description="最小进货单价"),
    max_price: Optional[float] = Query(None, ge=0, description="最大进货单价"),
    min_quantity: Optional[int] = Query(None, ge=1, description="最小进货数量"),
    max_quantity: Optional[int] = Query(None, ge=1, description="最大进货数量"),
    
    # 排序参数
    sort_by: Optional[str] = Query(None, 
                                  description="排序字段（order_date/purchase_price/quantity/total_amount）",
                                  regex="^(order_date|purchase_price|quantity|total_amount)$"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    
    # 分页参数
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    
    db: Session = Depends(get_db)
) -> PaginatedPurchaseResponse:
    # 基础查询
    query = db.query(db_models.PurchaseOrder)

    # 应用筛选条件
    if order_id:
        query = query.filter(db_models.PurchaseOrder.id==order_id)
    if book_isbn and book_isbn!='':
        if exact_isbn:
            query = query.filter(db_models.PurchaseOrder.book_isbn == book_isbn)
        else:
            query = query.filter(db_models.PurchaseOrder.book_isbn.contains(book_isbn))
    if payment_status:
        query = query.filter(db_models.PurchaseOrder.payment_status == payment_status)
    if operator_id and operator_id!='':
        if exact_operator_id:
            query = query.filter(db_models.PurchaseOrder.operator_id == operator_id)
        else:
            query = query.filter(db_models.PurchaseOrder.operator_id.contains(operator_id))
    if operator_id2 and operator_id2!="":
        if exact_operator_id2:
            query = query.filter(db_models.PurchaseOrder.operator_id2 == operator_id2)
        else:
            query = query.filter(db_models.PurchaseOrder.operator_id2.contains(operator_id2))
    if operator_id3 and operator_id3!="":
        if exact_operator_id3:
            query = query.filter(db_models.PurchaseOrder.operator_id3 == operator_id3)
        else:
            query = query.filter(db_models.PurchaseOrder.operator_id3.contains(operator_id3))
    if start_date:
        # 使用 DATE() 函数提取日期部分进行比较，确保精确到天
        query = query.filter(db_models.PurchaseOrder.order_date.cast(db.Date) >= start_date)
    if end_date:
        # 使用 DATE() 函数提取日期部分进行比较，确保精确到天
        query = query.filter(db_models.PurchaseOrder.order_date.cast(db.Date) <= end_date)
    if min_price is not None:
        query = query.filter(db_models.PurchaseOrder.purchase_price >= min_price)
    if max_price is not None:
        query = query.filter(db_models.PurchaseOrder.purchase_price <= max_price)
    if min_quantity is not None:
        query = query.filter(db_models.PurchaseOrder.quantity >= min_quantity)
    if max_quantity is not None:
        query = query.filter(db_models.PurchaseOrder.quantity <= max_quantity)

    # 处理排序
    sort_mapping = {
        "order_date": db_models.PurchaseOrder.order_date,
        "purchase_price": db_models.PurchaseOrder.purchase_price,
        "quantity": db_models.PurchaseOrder.quantity,
        "total_amount": db_models.PurchaseOrder.total_amount
    }
    
    if sort_by:
        order_column = sort_mapping.get(sort_by)
        order_func = desc if sort_order == "desc" else asc
        query = query.order_by(order_func(order_column))
    else:
        query = query.order_by(asc(db_models.PurchaseOrder.order_date))

    # 分页处理
    total = query.count()
    orders = query.offset((page - 1) * page_size).limit(page_size).all()

    # 构建响应数据
    items = [
        PurchaseOrderDetail(
            id=order.id,
            book_isbn=order.book_isbn,
            purchase_price=float(order.purchase_price),
            quantity=order.quantity,
            total_amount=float(order.total_amount),
            order_date=order.order_date,
            payment_status=order.payment_status,
            operator_id=order.operator_id,
            operator_id2=order.operator_id2,
            operator_id3=order.operator_id3
        ) for order in orders
    ]

    return PaginatedPurchaseResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )


@router.put("/pay/{order_id}", response_model=PaymentResponse)
def pay_purchase_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
)-> PaymentResponse:
    # 获取订单
    order = db.query(db_models.PurchaseOrder).filter(order_id==db_models.PurchaseOrder.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 状态校验
    if order.payment_status != "未付款":
        raise HTTPException(
            status_code=400,
            detail="订单状态不可付款"
        )
    
    # 更新订单状态
    order.payment_status = "已付款"
    order.operator_id2 = current_user.employee_id
    
    # 获取当前时间作为交易时间
    transaction_time = datetime.now()
    
    # 创建账单（添加transaction_time字段）
    bill = db_models.Bill(
        bill_type="进货",
        amount=order.total_amount,
        related_order=order.id,
        operator_id=current_user.employee_id,
        transaction_time=transaction_time
    )
    db.add(bill)
    
    # 更新库存
    # book = db.query(db_models.Book).filter_by(isbn=order.book_isbn).first()
    # book.stock += order.quantity
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"付款失败: {str(e)}"
        )
    
    return {"message": "付款成功", "order_id": order.id, "paid_amount": order.total_amount}

@router.put("/return/{order_id}", response_model=ReturnResponse)
def return_purchase_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
)-> ReturnResponse:
    # 获取订单
    order = db.query(db_models.PurchaseOrder).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 状态校验
    if order.payment_status != "未付款":
        raise HTTPException(
            status_code=400,
            detail="仅支持未付款订单退货"
        )
    
    # 更新状态
    order.payment_status = "已退货"
    order.operator_id2 = current_user.employee_id
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"退货失败: {str(e)}"
        )
    
    return {"message": "退货成功", "order_id": order.id}

@router.put("/arrive/{order_id}", response_model=PaymentResponse)
def arrive_purchase_order(
    order_id: int,
    retail_price:Optional[float]=Query(None, description="零售价"),
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
)-> PaymentResponse:
    # 获取订单
    order = db.query(db_models.PurchaseOrder).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    # 状态校验
    if order.payment_status!= "已付款":
        raise HTTPException(
            status_code=400,
            detail="仅支持已付款订单到货")
    
    # 更新状态
    order.payment_status = "已到货"
    order.operator_id3 = current_user.employee_id
    # 更新库存
    book = db.query(db_models.Book).filter_by(isbn=order.book_isbn).first()
    book.stock += order.quantity

    if (not hasattr(book,"retail_price") ) or book.retail_price is None or book.retail_price == 0:
        if retail_price is None:
            raise HTTPException(
                status_code=400,
                detail="未提供零售价"
            )
        book.retail_price = retail_price

    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="到货失败"
        ) 

    return {"message": "到货成功", "order_id": order.id, "paid_amount": order.total_amount}
