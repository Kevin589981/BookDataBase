from fastapi import APIRouter, Depends, HTTPException, Query, status,Response
from sqlalchemy.orm import Session
from typing import Optional
from server.database import get_db
from server.schemas.book_schemas import BookResponse, BookUpdateRequest, PaginatedBookResponse
from server import db_models
from server import auth
from sqlalchemy import desc, asc
router = APIRouter(prefix="/books", tags=["books"])

# get方法查询所有图书已完成
@router.get("/", response_model=PaginatedBookResponse,dependencies=[Depends(auth.Auth.get_current_user)])
def search_books(
    isbn: Optional[str] = Query(None, 
                               
                            
                               pattern="^[0-9]*$"),
    title: Optional[str] = Query(None,description="图书标题"),
    author: Optional[str] = Query(None,description="图书作者"),
    publisher: Optional[str] = Query(None,description="图书出版社"),
    exact_isbn: Optional[bool] = Query(False, description="ISBN精确匹配"),
    exact_title: Optional[bool] = Query(False, description="书名精确匹配"),
    exact_author: Optional[bool] = Query(False, description="作者精确匹配"),
    exact_publisher: Optional[bool] = Query(False, description="出版社精确匹配"),
    min_retail_price: Optional[float] = Query(None,ge=0.0,description="图书零售价"),
    max_retail_price: Optional[float] = Query(None,ge=0.0,description="图书零售价"),
    min_stock: Optional[int] = Query(None, 
                                    ge=0,
                                    description="最小库存量"),
    max_stock: Optional[int] = Query(None,
                                    ge=0,
                                    description="最大库存量"),
    sort_by: Optional[str] = Query(None, description="排序字段（isbn/title/author/publisher/retail_price/stock）"),
    sort_order: Optional[str] = Query("asc", description="排序方向（asc/desc）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
    # user=Depends(auth.Auth.get_current_user)
):
    """多条件图书查询"""
    query = db.query(db_models.Book)
    
    # 动态构建查询条件
    filters = []
    if isbn and isbn!="":
        if exact_isbn:
            
            filters.append(db_models.Book.isbn == isbn)
        else:
            filters.append(db_models.Book.isbn.contains(isbn))
    if title and title!="":
        if exact_title:
            filters.append(db_models.Book.title == title)
        else:
            filters.append(db_models.Book.title.contains(title))
    if author and author!="":
        if exact_author:
            filters.append(db_models.Book.author == author)
        else:
            filters.append(db_models.Book.author.contains(author)) 
    if publisher and publisher!="":
        if exact_publisher:
            filters.append(db_models.Book.publisher == publisher)
        else:
            filters.append(db_models.Book.publisher.contains(publisher))
    if min_retail_price is not None:
        filters.append(db_models.Book.retail_price >= min_retail_price)
    if max_retail_price is not None:
        filters.append(db_models.Book.retail_price <= max_retail_price)
    if min_stock is not None:
        filters.append(db_models.Book.stock >= min_stock)
    if max_stock is not None:
        filters.append(db_models.Book.stock <= max_stock)
    query = query.filter(*filters)

    if sort_by:
        if sort_by=="isbn":
            column=db_models.Book.isbn
        elif sort_by=="title":
            column=db_models.Book.title
        elif sort_by=="author":
            column=db_models.Book.author
        elif sort_by=="publisher":
            column=db_models.Book.publisher
        elif sort_by=="retail_price":
            column=db_models.Book.retail_price
        elif sort_by=="stock":
            column=db_models.Book.stock
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的排序字段"
            )
    
        query=query.order_by(desc(column) if sort_order == "desc" else column)
        
    
    # 执行分页查询
    total = query.count()
    books = query.offset((page-1)*page_size).limit(page_size).all()
    # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
    #     f.write(f"{[BookResponse.from_orm(book) for book in books]}\n")
    #     f.flush()
    return PaginatedBookResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=[BookResponse.from_orm(book) for book in books]
    )

#post方法创建图书已完成
@router.post("/", 
           response_model=BookResponse,
           dependencies=[Depends(auth.Auth.get_current_user)],
           status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookResponse,  
    db: Session = Depends(get_db)
):
    """创建新图书"""
    # with open(r"D:\Projects\DataBase\debug.json","w") as f:
    #     f.write(f"{123456}\n")
    #     f.flush()
    # ISBN唯一性校验

    if db.query(db_models.Book).filter(db_models.Book.isbn == book_data.isbn).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ISBN已存在"
        )
    

    # 自动处理默认值
    book_dict = book_data.dict()
    book_dict.setdefault("stock", 0)  # 确保stock有默认值
    
    try:
        new_book = db_models.Book(**book_dict)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
    except Exception as e:
        # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
        #     f.write(f"{str(e)}\n")
        #     f.flush()
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e.orig) if hasattr(e, "orig") else "数据库错误"
        )
    
    return new_book
   
@router.delete(
    "/{isbn}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "图书不存在"},
        403: {"description": "权限不足"},
        400: {"description": "无效的ISBN格式"}
    }
)
def delete_book(
    isbn: str,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
):
    """
    删除图书（需要管理员权限）
    - 13位数字的国际标准书号
    """
    # ISBN格式验证
    if len(isbn) != 13 or not isbn.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的ISBN格式"
        )

    # 获取图书对象
    book = db.query(db_models.Book).filter(db_models.Book.isbn == isbn).first()
    if not book: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图书不存在"
        )
    purchase_order=db.query(db_models.PurchaseOrder).filter(db_models.PurchaseOrder.book_isbn==isbn).first()
    if purchase_order:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="存在关联记录，无法删除"
        )
    sale_order=db.query(db_models.SaleOrder).filter(db_models.SaleItem.book_isbn==isbn).first()
    if sale_order:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="存在关联记录，无法删除"
        )
    try:
        db.delete(book)
        db.commit()
    except Exception as e:
        db.rollback()
        # 处理外键约束错误
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="存在关联记录，无法删除"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败: {str(e)}"
        )

    return Response(status_code=status.HTTP_200_OK)


@router.put("/{isbn}", response_model=BookResponse)
def update_book_info(
    isbn: str,
    update_data: BookUpdateRequest,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(auth.Auth.get_current_user)
):
    """更新图书信息"""
    # 参数验证
    if len(isbn) != 13 or not isbn.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的ISBN格式（需要13位数字）"
        )
    
    # 获取图书对象
    book = db.query(db_models.Book).filter(db_models.Book.isbn == isbn).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图书不存在"
        )
    
    # 动态更新字段
    update_dict = update_data.dict(exclude_unset=True)
    for field in ["title", "author", "publisher", "retail_price", "stock"]:
        if field in update_dict:
            # 特殊处理价格字段
            if field == "retail_price" and update_dict[field]!=None and update_dict[field] <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="价格必须大于0"
                )
            setattr(book, field, update_dict[field])
    
    # 库存非负校验
    if book.stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="库存不能为负数"
        )
    
    try:
        db.commit()
        db.refresh(book)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库更新失败: {str(e)}"
        )
    
    return book