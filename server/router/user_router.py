from fastapi import APIRouter, Depends, HTTPException,Query,status
from sqlalchemy.orm import Session
from server import db_models, auth
from server.database import get_db
from typing import Optional
from server.schemas.user_schemas import LoginRequest, LoginResponse, LogoutResponse,UserCreate, UserResponse, PaginatedUserResponse,UserUpdateRequest, AdminUserUpdateRequest
from datetime import datetime, timedelta, timezone
from sqlalchemy import desc, asc
import json
router = APIRouter(tags=["users"])

# 后续必须要禁用，这是默认管理员注册
@router.post("/users/adminsignup",response_model=UserResponse)
async def create_default_admin(
    db: Session = Depends(get_db)
)->UserResponse:
    """创建默认的超级管理员账户"""
    with open(r'./server/dat/user_default.json', 'r', encoding='utf-8') as file:
        info = json.load(file)
    if not info["accessible"]:
        raise HTTPException(status_code=403, detail="该创建用户接口已关闭，请联系管理员")
    datas = info["datas"]
    try:    
        
        for data in datas:
            admin = db.query(db_models.User).filter(db_models.User.username==data["default_super_username"]).first()
            
            if not admin:

                admin = db_models.User(
                    username=data["default_super_username"],
                    employee_id=data["default_employee_id"],
                    true_name=data["default_true_name"],
                    gender=data["default_gender"],
                    age=data["default_age"],
                    password_hash=auth.Auth.get_password_hash(data["default_super_password"]),
                    isSuperAdmin=data["default_isSuperAdmin"]
                )
                
                db.add(admin)
                db.commit()
    except Exception as e:
        # with open(r"D:\Projects\DataBase\debug.txt","w") as f:
        #     f.write(f"create_default_super_user_error{str(e)}")
        #     f.flush()
        raise HTTPException(status_code=500, detail="创建超级管理员账户失败")
    # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
    #     f.write("create_default_super_user\n")
    #     f.flush()
    if (info["default_return"]):
        return UserResponse(
            username= datas[0]["default_super_username"],
            employee_id= datas[0]["default_employee_id"],
            true_name= datas[0]["default_true_name"],
            gender= datas[0]["default_gender"],
            age= datas[0]["default_age"],
            isSuperAdmin= datas[0]["default_isSuperAdmin"]
        )
    else:
        # 为了掩盖注册接口，返回空用户信息
        return UserResponse(
            username="",
            employee_id= "",
            true_name= "",
            gender= "",
            age= 0,
            isSuperAdmin= False
        )
## 注册接口已完成，用户已经注册过则会返回400错误码，正常注册则返回200
@router.post("/users/register",response_model=UserResponse,dependencies=[Depends(auth.Auth.admin_required)])
async def create_user(
    request: UserCreate,
    db: Session = Depends(get_db)
)->UserResponse:
    user = db.query(db_models.User).filter(db_models.User.username == request.username).first()
    if user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = db.query(db_models.User).filter(db_models.User.employee_id== request.employee_id).first()
    if user:
        raise HTTPException(status_code=400, detail="工号已存在")
    user = db_models.User(
        username=request.username,
        employee_id=request.employee_id,
        true_name=request.true_name,
        gender=request.gender,
        age=request.age,
        password_hash=auth.Auth.get_password_hash(request.password),
        isSuperAdmin=request.isSuperAdmin
    )
    db.add(user)
    db.commit()
    return UserResponse(
        username=user.username,
        employee_id=user.employee_id,
        true_name=user.true_name,
        gender=user.gender,
        age=user.age,
        isSuperAdmin=user.isSuperAdmin
    )

@router.delete("/users/{username}",response_model=UserResponse,dependencies=[Depends(auth.Auth.admin_required)])
async def delete_user(
    username: str,
    db: Session = Depends(get_db)
)->UserResponse:
    # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
    #     f.write(f"\n12345\n")
    #     f.flush()
    try:
        user = db.query(db_models.User).filter(db_models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        if user.isSuperAdmin:
            raise HTTPException(status_code=403, detail="无法删除超级管理员")
        loginedUser=db.query(db_models.LoginedUser).filter(db_models.LoginedUser.username == username).first()
        db.delete(user)
        if (loginedUser):
            db.delete(loginedUser)
        db.commit()
        return UserResponse(
            username=user.username,
            employee_id=user.employee_id,
            true_name=user.true_name,
            gender=user.gender,
            age=user.age,
            isSuperAdmin=user.isSuperAdmin
        )
    except Exception as e:
        # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
        #     f.write(f"{str(e)}")
        #     f.flush()
        raise HTTPException(status_code=400, detail="删除用户失败")

## 已完成登录接口
@router.post("/login",response_model=LoginResponse)
async def login(request: LoginRequest, 
                db: Session = Depends(get_db))->LoginResponse:
    try:
        user = db.query(db_models.User).filter(db_models.User.username == request.username).first()
    except Exception as e:
        # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
        #     f.write(f"{str(e)}")
        #     f.flush()
        raise HTTPException(status_code=500, detail="数据库查询失败") 
    # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
    #         f.write(f"THere!\n")
    #         f.flush()  
    if not user or not \
        auth.Auth.verify_password(\
            request.password, user.password_hash):
        
        raise HTTPException(status_code=401, detail="无效的用户名或密码")
    # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
    #         f.write(f"Here!\n")
    #         f.flush()
    try:
    # 账号密码验证通过后，生成token并返回
        expire =datetime.now(timezone.utc) + timedelta(hours=8)
        access_token= auth.Auth.create_access_token(db,user)
    except Exception as e:
        # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
        #         f.write(f"{str(e)}")
        #         f.flush()
        raise HTTPException(status_code=500, detail="创建token失败")
    return LoginResponse(
            access_token= access_token, 
            token_type= "bearer",
            expiration_time=expire.timestamp(),
            user_info=UserResponse(
                username= user.username,
                employee_id= user.employee_id,
                true_name= user.true_name,
                gender= user.gender,
                age= user.age,
                isSuperAdmin= user.isSuperAdmin
            ))
## 已完成注销接口
@router.post("/logout",response_model=LogoutResponse)
async def logout(logined_user: db_models.LoginedUser=Depends(auth.Auth.get_current_user),
                 db: Session = Depends(get_db))->LogoutResponse:
    # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
    #     f.write(f"12345\n")
    #     f.flush()
    try:
        db.delete(logined_user)
        db.commit()
        return LogoutResponse(message= "注销成功")
    except Exception as e:
        # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
        #     f.write(f"{str(e)}")
        #     f.flush()
        raise HTTPException(status_code=500, detail="注销失败")
## 已完成获取当前用户信息接口
@router.get("/me",response_model=UserResponse)
async def get_current_user_info(
    logined_user: db_models.LoginedUser=Depends(auth.Auth.get_current_user),
    db: Session = Depends(get_db)
)->UserResponse:
    myself=db.query(db_models.User).filter(db_models.User.username == logined_user.username).first()
    return UserResponse(
        username= myself.username,
        employee_id= myself.employee_id,
        true_name=myself.true_name, 
        gender=myself.gender, 
        age=myself.age,
        isSuperAdmin=myself.isSuperAdmin
    )

## 已完成获取所有用户信息接口
@router.get("/users/all", response_model=PaginatedUserResponse,dependencies=[Depends(auth.Auth.admin_required)])
async def get_all_users(
    # 筛选参数
    username: Optional[str] = Query(None, description="按姓名搜索"),
    employee_id: Optional[str] = Query(None, description="按工号搜索"),
    true_name: Optional[str] = Query(None, description="按真实姓名搜索"),
    exact_username: Optional[bool] = Query(False, description="用户名精确匹配"),
    exact_employee_id: Optional[bool] = Query(False, description="工号精确匹配"),
    exact_true_name: Optional[bool] = Query(False, description="真实姓名精确匹配"),
    gender: Optional[str] = Query(None, description="按性别筛选", pattern="^(male|female)$"),
    min_age: Optional[int] = Query(None, ge=0, description="最小年龄"),
    max_age: Optional[int] = Query(None, ge=0, description="最大年龄"),
    
    # 排序参数
    sort_by: Optional[str] = Query(None, description="排序字段（username/age/employee_id）"),
    sort_order: Optional[str] = Query("asc", description="排序方向（asc/desc）"),
    
    # 分页参数
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    
    db: Session = Depends(get_db)
)->PaginatedUserResponse:
    # 基础查询
    query = db.query(db_models.User)
    
    # 应用筛选条件
    if username:
        if exact_username:
            query = query.filter(db_models.User.username == username)
        else:
            query = query.filter(db_models.User.username.contains(username))
    if employee_id:
        if exact_employee_id:
            query = query.filter(db_models.User.employee_id == employee_id)
        else:
            query = query.filter(db_models.User.employee_id.contains(employee_id))
    if true_name:
        if exact_true_name:
            query = query.filter(db_models.User.true_name == true_name)
        else:
            query = query.filter(db_models.User.true_name.contains(true_name))
    if gender:
        query = query.filter(db_models.User.gender == gender)
    if min_age is not None:
        query = query.filter(db_models.User.age >= min_age)
    if max_age is not None:
        query = query.filter(db_models.User.age <= max_age)
    
    # 应用排序
    if sort_by:
        if sort_by=="username":
            column=db_models.User.username
        elif sort_by=="age":
            column=db_models.User.age
        else :
            column=db_models.User.employee_id
        query = query.order_by(desc(column)if sort_order=='desc' else asc(column))
    
    # 分页处理
    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 构建响应
    return PaginatedUserResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[
        UserResponse(
            username=user.username,
            employee_id=user.employee_id,
            true_name=user.true_name,
            gender=user.gender,
            age=user.age,
            isSuperAdmin=user.isSuperAdmin
        ) for user in users]
    )

@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserUpdateRequest,
    current_user: db_models.LoginedUser = Depends(auth.Auth.get_current_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    # 获取数据库用户对象
    db_user = db.query(db_models.User).filter(
        db_models.User.username == current_user.username
    ).first()
    # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
    #     f.write(f"update_data:{update_data}\n{db_user}")
    #     f.flush()
    # 密码修改逻辑
    if update_data.new_password:
        if not update_data.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="修改密码需要提供当前密码"
            )
        
        # 验证当前密码
        if not auth.Auth.verify_password(
            update_data.current_password, 
            db_user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="当前密码验证失败"
            )
        
        # 更新密码哈希
        db_user.password_hash = auth.Auth.get_password_hash(update_data.new_password)

    # 更新其他字段
    update_dict = update_data.dict(exclude_unset=True, exclude={"current_password", "new_password"})
    for key, value in update_dict.items():
        if value is not None:
            if (key=="isSuperAdmin" and value==False):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="非超级管理员不能修改为超级管理员"
                )
            if (key=="employee_id" and db_user.isSuperAdmin==False):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="非超级管理员不能修改工号"
                )
            setattr(db_user, key, value)

    # 验证年龄范围
    if update_data.age is not None and update_data.age < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年龄不能为负数"
        )

    # 验证性别选项
    valid_genders = ["male", "female"]
    if update_data.gender and update_data.gender not in valid_genders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的性别选项，可选值：{', '.join(valid_genders)}"
        )

    if update_dict:
        db.query(db_models.LoginedUser).filter(
            db_models.LoginedUser.username == current_user.username
        ).update({
            db_models.LoginedUser.username: db_user.username,
            db_models.LoginedUser.employee_id: db_user.employee_id,
            db_models.LoginedUser.isSuperAdmin: db_user.isSuperAdmin
        })
    try:
        db.commit()
        db.refresh(db_user)
        return UserResponse(
            username=db_user.username,
            employee_id=db_user.employee_id,
            true_name=db_user.true_name,
            gender=db_user.gender,
            age=db_user.age,
            isSuperAdmin=db_user.isSuperAdmin
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户信息失败：{str(e)}"
        )

@router.patch("/users/{username}", response_model=UserResponse, dependencies=[Depends(auth.Auth.admin_required)])
async def update_user(
    username: str,
    update_data: AdminUserUpdateRequest,
    db: Session = Depends(get_db)
) -> UserResponse:
    # 获取数据库用户对象
    db_user = db.query(db_models.User).filter(
        db_models.User.username == username
    ).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 如果需要重置密码
    if update_data.reset_password:
        db_user.password_hash = auth.Auth.get_password_hash(username)
    
    # 更新其他字段
    update_dict = update_data.dict(exclude_unset=True, exclude={"reset_password"})
    for key, value in update_dict.items():
        if value is not None:
            setattr(db_user, key, value)
    
    # 验证年龄范围
    if update_data.age is not None and update_data.age < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年龄不能为负数"
        )
    
    # 验证性别选项
    valid_genders = ["male", "female"]
    if update_data.gender and update_data.gender not in valid_genders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的性别选项，可选值：{', '.join(valid_genders)}"
        )
    
    # 更新登录用户表中的相关信息
    logined_user = db.query(db_models.LoginedUser).filter(
        db_models.LoginedUser.username == username
    ).first()
    
    if logined_user and update_dict:
        db.query(db_models.LoginedUser).filter(
            db_models.LoginedUser.username == username
        ).update({
            db_models.LoginedUser.username: db_user.username,
            db_models.LoginedUser.employee_id: db_user.employee_id,
            db_models.LoginedUser.isSuperAdmin: db_user.isSuperAdmin
        })
    
    try:
        db.commit()
        db.refresh(db_user)
        return UserResponse(
            username=db_user.username,
            employee_id=db_user.employee_id,
            true_name=db_user.true_name,
            gender=db_user.gender,
            age=db_user.age,
            isSuperAdmin=db_user.isSuperAdmin
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户信息失败：{str(e)}"
        )