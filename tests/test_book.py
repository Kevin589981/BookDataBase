import requests
import pytest
from typing import Dict

BASE_URL = "http://localhost:8000/"
auth_token: str = ""  # 全局认证令牌

# 用户登录模块



test_book: Dict = {
    "isbn": "9787111633333",
    "title": "Python编程从入门到实践",
    "author": "Eric Matthes",
    "publisher": "人民邮电出版社",
    "retail_price": 89.0,
    "stock": 10
}
auth_token: str = ""  # 全局认证令牌
def test_admin_login():
    """测试管理员登录并获取token"""
    global auth_token
    
    payload = {
        'username': 'admin',
        'password': 'admin'
    }
    response = requests.post(
        f'{BASE_URL}/login',
        json=payload
    )
    
    assert response.status_code == 200, "登录状态码异常"
    assert 'access_token' in response.json(), "响应缺少token"
    
    auth_token = response.json()['access_token']
    # with open(r"D:\Projects\DataBase\debug.txt","a") as f:
    #     f.write(f"\n{auth_token}\n")
    #     f.flush()
    assert len(auth_token) > 100, "token长度异常"

def test_create_book():
    """测试创建新图书"""
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f'{BASE_URL}/books/',
        json=test_book,
        headers=headers
    )
    # with open(r"D:\Projects\DataBase\debug.txt","w") as f:
    #     f.write(f"{auth_token}\n{response.json()}\n")
    #     f.flush()
    assert response.status_code == 201, "创建失败"
    assert response.json()["isbn"] == test_book["isbn"], "ISBN不匹配"

# def test_search_books():
#     """测试多条件查询"""
#     params = {
#         "title": "Python",
#         "min_stock": 5
#     }
    
#     response = requests.get(
#         f'{BASE_URL}/books/',
#         params=params
#     )
    
#     assert response.status_code == 200, "查询失败"
#     assert isinstance(response.json()["data"], list), "返回数据类型错误"
#     assert len(response.json()["data"]) >= 1, "未找到预期图书"

# def test_update_book():
#     """测试更新图书信息"""
#     headers = {
#         "Authorization": f"Bearer {auth_token}",
#         "Content-Type": "application/json"
#     }
    
#     update_data = {
#         "retail_price": 99.9,
#         "stock": 20
#     }
    
#     response = requests.put(
#         f'{BASE_URL}/books/{test_book["isbn"]}',
#         json=update_data,
#         headers=headers
#     )
    
#     assert response.status_code == 200, "更新失败"
#     assert response.json()["retail_price"] == 99.9, "价格未更新"
#     assert response.json()["stock"] == 20, "库存未更新"

# def test_duplicate_create():
#     """测试重复创建冲突"""
#     headers = {
#         "Authorization": f"Bearer {auth_token}",
#         "Content-Type": "application/json"
#     }
    
#     response = requests.post(
#         f'{BASE_URL}/books/',
#         json=test_book,
#         headers=headers
#     )
    
#     assert response.status_code == 409, "重复创建未触发冲突"

# # 错误场景测试
# def test_unauthorized_access():
#     """测试未授权访问"""
#     response = requests.post(
#         f'{BASE_URL}/books/',
#         json={
#             "isbn": "9787115464456",
#             "title": "测试图书",
#             "retail_price": 50.0
#         }
#     )
    
#     assert response.status_code == 401, "未正确验证权限"

def test_delete_book():
    """测试删除功能"""
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    # # 先创建测试数据
    # test_isbn = "9787115464456"
    # create_response = requests.post(
    #     f'{BASE_URL}/books/',
    #     json={
    #         "isbn": 9787111633333,
    #         "title": "测试删除用书",
    #         "retail_price": 50.0
    #     },
    #     headers=headers
    # )
    # assert create_response.status_code == 201

    # 执行删除
    delete_response = requests.delete(
        f'{BASE_URL}/books/{9787111633333}',
        headers=headers
    )
    assert delete_response.status_code == 204

    # 验证已删除
    get_response = requests.get(f'{BASE_URL}/books',params={"isbn": 9787111633333})
    assert len(get_response.json()["data"])==0

def test_delete_protected():
    """测试删除保护机制"""
    # 尝试删除不存在的书 
    response = requests.delete(
        f'{BASE_URL}/books/0000000000000',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404

    # 尝试无权限删除
    response = requests.delete(
        f'{BASE_URL}/books/{9787111633333}'
    )
    assert response.status_code == 401