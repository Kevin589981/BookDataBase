from datetime import datetime, timedelta,timezone
from functools import wraps
import hashlib
import jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from server.db_models import User,LoginedUser
from server.database import get_db
SECRET_KEY = "The-Project-Is-Made-By-Kevin"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Auth:
    # 返回密码的md5哈希值（TODO：用于创建账户时加密）
    @staticmethod
    def get_password_hash(password: str) -> str:
        return hashlib.md5(password.encode()).hexdigest()
    
    # 验证密码是否匹配
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return hashlib.md5(plain_password.encode()).hexdigest() == hashed_password
    # TODO: 识别toke适配逻辑
    @staticmethod
    def create_access_token(db:Session, user:User) -> str:
        expire = datetime.now(timezone.utc) + timedelta(hours=8)
        token_data={
            "username":user.username,
            #"isSuperAdmin":user.isSuperAdmin,
            "expiration_time":expire.timestamp()
        }
        token=jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        db.query(LoginedUser).filter(LoginedUser.username==user.username).delete()
        db.add(LoginedUser(username=user.username,
                           employee_id=user.employee_id,
                           isSuperAdmin=user.isSuperAdmin,
                           token=token,
                           expiration_time=expire))
        db.commit()
        return token
    # 根据token，获得当前用户名称、身份、权限(LoginedUser表)
    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), 
                         db: Session = Depends(get_db))->LoginedUser:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭据或登录过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
        #     # f.write(f"username:{username}\n")
        #     f.write(f"token:{token}\n")
        #     f.flush()
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            ## 
            username:str = payload.get("username")
            ## 已舍弃username字段进行校验的机制，考虑到username可能会被修改
            if username is None:
                # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
                #     f.write(f"{str(e)}\n")
                #     f.flush()
                raise credentials_exception

        except jwt.PyJWTError as e:
            raise credentials_exception
        
        # 每次进行操作前删除过期的token
        db.query(LoginedUser).filter(datetime.now(timezone.utc)>LoginedUser.expiration_time).delete()
        logined_user = db.query(LoginedUser).filter(
            LoginedUser.token==token).first()
        if logined_user is None:
            # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
            #     f.write(f"There is None\n")
            #     f.flush()
            raise credentials_exception
        return logined_user

   
    @staticmethod
    def admin_required(
        logined_user: LoginedUser = Depends(get_current_user),
    ):
        try:
            if not logined_user.isSuperAdmin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="权限不足",
                )
            return logined_user
        except Exception as e:
            # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
            #     f.write(f"{str(e)}\n")
            #     f.flush()
            raise e
        