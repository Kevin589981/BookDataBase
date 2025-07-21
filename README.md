# 图书管理系统 (Vue版)

If you have a windows machine, you can just run the file `run.bat` after installing the dependencies.

## 系统概述
基于Vue 3 + Vite + Element Plus实现的前后端分离图书管理系统，包含用户权限管理、图书库存管理、财务流水等核心功能模块。

## 技术栈
- 前端：Vue 3 + Vite + Element Plus + Axios
- 后端：Python FastAPI (原README中提到的API接口保持不变)
- 数据库：SQLAlchemy

## 目录结构 (前端部分)
```
frontend/
├── src/
│   ├── assets/            # 静态资源
│   ├── components/        # 公共组件
│   │   ├── bill/          # 财务相关组件
│   │   ├── book/          # 图书相关组件
│   │   ├── purchase/      # 进货相关组件
│   │   ├── sale/          # 销售相关组件
│   │   └── user/          # 用户相关组件
│   ├── router/            # 路由配置
│   ├── services/          # API服务
│   ├── utils/             # 工具函数
│   ├── views/             # 页面视图
│   │   ├── BillsView.vue   # 财务管理
│   │   ├── BooksView.vue   # 图书管理
│   │   ├── DashboardView.vue # 仪表盘
│   │   ├── LoginView.vue   # 登录页面
│   │   ├── PurchaseView.vue # 进货管理
│   │   ├── SaleView.vue    # 销售管理
│   │   └── UsersView.vue   # 用户管理
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── vite.config.js         # Vite配置
└── package.json           # 项目依赖
```

## 核心功能模块

### 1. 用户管理系统
- 实现两级权限管理（超级管理员/普通管理员）
- 使用JWT进行用户认证
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

## 安装运行
### 前端
```bash
cd frontend
npm install
npm run dev
```

### 后端
```bash
pip install -r requirements.txt
uvicorn server.main:app --reload
```

## API接口文档
查看localhost:<端口号>/docs