from fastapi import FastAPI
from server.router import user_router, book_router, purchase_order_router,\
    sale_order_router,bill_router
from server.database import engine
from server import db_models

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World",
            "Introduction":"This is a book management system designed by Kevin(Fudan University)."}

# 数据库表结构初始化
db_models.Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)
app.include_router(book_router.router)
app.include_router(purchase_order_router.router)
app.include_router(sale_order_router.router)
app.include_router(bill_router.router)

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host=localhost, port=8000)

    #uvicorn server.main:app --reload
    #需要激活虚拟环境