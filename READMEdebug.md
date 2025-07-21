## 一开始想用Streamlit写前端做的，然后这个是一开始的框架计划，但是后来爆改，用了vue写前端，所以这个文档相当于没什么用
## 一开始想用Streamlit写前端做的，然后这个是一开始的框架计划，但是后来爆改，用了vue写前端，所以这个文档相当于没什么用
## 一开始想用Streamlit写前端做的，然后这个是一开始的框架计划，但是后来爆改，用了vue写前端，所以这个文档相当于没什么用
## 一开始想用Streamlit写前端做的，然后这个是一开始的框架计划，但是后来爆改，用了vue写前端，所以这个文档相当于没什么用

# 图书管理系统

## 系统概述
基于Streamlit+SQLite实现的图书管理系统，采用前后端分离架构，包含用户权限管理、图书库存管理、财务流水等核心功能模块。

## 目录结构
```
├── server/               # 后端服务模块
│   ├── db_models.py      # 数据库模型定义（用户/图书/账单）
│   ├── api.py            # RESTful API接口
│   └── auth.py           # 用户认证与权限管理
├── client/               # 前端界面模块
│   ├── app.py            # 主程序入口
│   ├── user_manage.py    # 用户管理界面
│   ├── book_manage.py    # 图书管理界面
│   └── finance.py        # 财务流水界面
├── database/             # 数据库文件
│   └── bookstore.db     # SQLite数据库
├── docs/                 # 文档资料
└── requirements.txt     # 依赖库列表
```

## 核心功能模块

### 1. 用户管理系统
- 实现两级权限管理（超级管理员/普通管理员）
- 使用MD5加密存储密码
- 用户字段：工号、姓名、性别、年龄、角色类型

### 2. 图书库存管理
- ISBN唯一标识图书
- 字段包括：书名、出版社、作者、零售价、库存量
- 支持多条件组合查询

### 3. 进销存管理
- 进货流程：创建订单→付款确认→库存更新
- 销售模块：实时更新库存，记录销售流水
- 退货处理：未付款订单可撤回

### 4. 财务管理系统
- 自动记录每笔交易的资金流水
- 支持按时间段查询收支明细
- 关联图书进货付款和销售收款

## 数据库设计
- users表：存储用户信息及加密密码
- books表：图书基本信息及库存状态
- orders表：进货订单记录（含付款状态）
- bills表：财务流水明细（类型/金额/时间）

## 安装运行
```bash
pip install -r requirements.txt
streamlit run client/app.py
```

## API接口文档

### 用户认证
- **POST /login**  
  用户登录  
  Request Body:
  ```json
  {
    "employee_id": "工号",
    "password": "密码"
  }
  ```
  权限要求：公开

### 图书管理
- **POST /books**  
  添加新图书  
  Request Body:
  ```json
  {
    "isbn": "图书ISBN",
    "title": "书名",
    "publisher": "出版社",
    "author": "作者",
    "price": 价格,
    "stock": 库存数量
  }
  ```
  权限要求：超级管理员

### 订单管理
- **POST /orders**  
  创建进货订单  
  Request Body:
  ```json
  {
    "book_isbn": "图书ISBN",
    "quantity": 进货数量,
    "operator_id": 操作员ID
  }
  ```
  权限要求：超级管理员

### 财务管理
- **GET /finance**  
  查询财务流水  
  Query Parameters:
  ```
  start=起始时间&end=结束时间
  ```
  权限要求：管理员

### 用户管理（待实现）
- **GET /users** 获取用户列表
- **POST /users** 创建新用户
- **PUT /users/{id}** 更新用户信息
- **DELETE /users/{id}** 删除用户

### 退货操作（待实现）
- **POST /returns** 创建退货订单
- **PUT /orders/{id}/status** 更新订单状态