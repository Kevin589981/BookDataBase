from pydantic import BaseModel, Field
from typing import Optional,List
from datetime import datetime

class UserResponse(BaseModel):
    username: str
    employee_id: str
    true_name: str
    gender: str
    age: int
    isSuperAdmin: bool

class UserCreate(BaseModel):
    username: str 
    employee_id: str = Field(...,min_length=1,max_length=20)
    true_name: str = Field(...,min_length=1,max_length=50)
    gender: str
    age: int = Field(...,ge=0)
    password: str = Field(...,min_length=6,max_length=20)
    isSuperAdmin: bool = Field(...,description="是否为管理员")

class PaginatedUserResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[UserResponse]

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: UserResponse
    expiration_time: datetime

class LogoutResponse(BaseModel):
    message: str

class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    true_name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    employee_id: Optional[str] = None
    isSuperAdmin: Optional[bool] = None
    current_password: Optional[str] = None  # 修改密码时需要验证
    new_password: Optional[str] = None

class AdminUserUpdateRequest(BaseModel):
    employee_id: Optional[str] = None
    true_name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    isSuperAdmin: Optional[bool] = None
    reset_password: Optional[bool] = False