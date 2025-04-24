from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Numeric,CheckConstraint,Enum,Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String(50),primary_key=True,unique=True,nullable=False)
    employee_id = Column(String(20), unique=True, nullable=False)  # 工号，采用字符串考虑到可以加部门
    true_name = Column(String(50), nullable=False)
    gender = Column(Enum('male', 'female'), nullable=False)
    age = Column(Integer)
    isSuperAdmin = Column(Boolean, nullable=False)  # 角色类型
    password_hash = Column(String(128), nullable=False)  # MD5加密后的密码


class LoginedUser(Base):
    __tablename__ = 'logined_users'
    username = Column(String(50), primary_key=True, nullable=False)
    employee_id = Column(String(20),unique=True,nullable=False)
    isSuperAdmin = Column(Boolean, nullable=False)
    token = Column(String(256), nullable=False)
    expiration_time = Column(DateTime, nullable=False)

class Book(Base):
    __tablename__ = 'books'
    
    isbn = Column(String(13), primary_key=True)
    title = Column(String(100), nullable=False)
    publisher = Column(String(100),nullable=True)
    author = Column(String(50),nullable=True)
    retail_price = Column(Numeric(10,2), nullable=True)
    stock = Column(Integer, default=0)
    __table_args__ = (
        CheckConstraint("LENGTH(isbn) = 13 AND isbn GLOB '[0-9]*'", name='valid_isbn'),
        CheckConstraint("retail_price > 0", name='positive_price'),
        CheckConstraint("stock >= 0", name='non_negative_stock')
    )
# class Order(Base):
#     __tablename__ = 'orders'
    
#     id = Column(Integer, primary_key=True,autoincrement=True)
#     book_isbn = Column(String(13), ForeignKey('books.isbn'))
#     quantity = Column(Integer, nullable=False)
#     total_amount = Column(Numeric(10,2), nullable=False)
#     order_date = Column(DateTime, default=datetime.now)
#     payment_status = Column(Enum("未付款","已付款","已退货","已到货"), default='未付款')
#     operator_id = Column(Integer, ForeignKey('users.employee_id'))

class PurchaseOrder(Base):
    __tablename__ = 'purchase_orders'
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    book_isbn = Column(String(13), ForeignKey('books.isbn', onupdate="CASCADE"), nullable=False)
    purchase_price = Column(Numeric(10,2), CheckConstraint("purchase_price > 0"))  # 进货价格
    quantity = Column(Integer, CheckConstraint("quantity > 0"), nullable=False) # 数量
    total_amount = Column(Numeric(10,2), CheckConstraint("total_amount > 0")) # 总价
    order_date = Column(DateTime, default=datetime.now)
    payment_status = Column(Enum("未付款","已付款","已退货","已到货"), default='未付款')
    operator_id = Column(String(20), ForeignKey('users.employee_id'),nullable=False)
    operator_id2 = Column(String(20),ForeignKey('users.employee_id'),nullable=True) #付款操作员/退货操作员
    operator_id3= Column(String(20),ForeignKey('users.employee_id'),nullable=True) #到货操作员
    __table_args__ = (
        CheckConstraint(
            "(operator_id2 IS NULL AND payment_status == '未付款') OR "
            "(operator_id2 IS NOT NULL AND payment_status != '未付款')"
        ),
        CheckConstraint(
            "(operator_id3 IS NULL AND payment_status != '已到货') OR "
            "(operator_id3 IS NOT NULL AND payment_status == '已到货')"
        ),
    )

# 销售订单表（记录实际销售信息）
class SaleOrder(Base):
    __tablename__ = 'sale_orders'
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    transaction_no = Column(String(32), unique=True)  # 交易流水号
    total_amount = Column(Numeric(10,2), CheckConstraint("total_amount > 0"))
    payment_method = Column(Enum("现金","银行卡","移动支付"),nullable=True)
    sold_items = relationship("SaleItem", back_populates="order")
    operator_id = Column(String(20), ForeignKey('users.employee_id'),nullable=True)# 操作员
    created_at = Column(DateTime, default=datetime.now)  # 添加创建时间字段
    
    
# 销售明细表（记录价格快照）
class SaleItem(Base):
    __tablename__ = 'sale_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('sale_orders.id', ondelete="CASCADE"))
    book_isbn = Column(String(13), ForeignKey('books.isbn', onupdate="CASCADE"))
    quantity = Column(Integer, CheckConstraint("quantity > 0"))
    sold_price = Column(Numeric(10,2), CheckConstraint("sold_price > 0"))  # 销售时价格
    total_amount = Column(Numeric(10,2), CheckConstraint("total_amount > 0"))  # 这一个项目的总价
    order = relationship("SaleOrder", back_populates="sold_items")

class Bill(Base):
    __tablename__ = 'bills'
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    bill_type = Column(Enum("进货","零售"), nullable=False)  # 资金流向
    amount = Column(Numeric(10,2), CheckConstraint("amount > 0"))
    transaction_time = Column(DateTime, default=datetime.now())
    related_order = Column(Integer)  # 通用订单ID
    operator_id = Column(String(20), ForeignKey('users.employee_id'),nullable=True)
    # 付款操作员，对应其他表的operator_id2
    __table_args__ = (
        CheckConstraint(
            "(bill_type IS NULL AND related_order IS NULL) OR "
            "(bill_type IS NOT NULL AND related_order IS NOT NULL)",
            name='order_relation_check'
        ),
    )
