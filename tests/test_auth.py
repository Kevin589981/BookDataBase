import requests
import pytest

BASE_URL = 'http://localhost:8000'
# def test_register_user():
#     # 注册用户测试
#     response = requests.post(f'{BASE_URL}/users/adminsignup')
#     # with open('debug.json', 'w') as f:
#     #     f.write(response.text)
#     # print(response.json())
#     assert response.status_code == 200
#     admin = response.json()
#     assert admin['employee_id'] == 'CS123456'
#     assert admin['username'] == 'admin'
#     assert admin['isSuperAdmin'] == True

auth_token :str  # 全局变量，用于存储 token
def test_successful_login():
    # 正常登录测试
    payload = {
        'username': 'admin',
        'password': 'admin'
    }
    response = requests.post(f'{BASE_URL}/login', json=payload)
    
    global auth_token
    auth_token=response.json()['access_token']
    assert response.status_code == 200
    assert auth_token is not None
    # with open('debug.json', 'a') as f:
    #     f.write(auth_token)
    # print(auth_token)
    assert 'username' in response.json()["user_info"]

# def test_wrong_password():
#     # 错误密码测试
#     payload = {
#         'username': 'admin',       ####这里的emplyee_id要改成username
#         'password': 'wrongpassword'
#     }
#     response = requests.post(f'{BASE_URL}/login', json=payload)
    
#     assert response.status_code == 401
#     assert '无效的用户名或密码' in response.json()['detail']


# def test_invalid_employee_id():
#     # 无效工号测试
#     payload = {
#         'username': '9999',
#         'password': 'admin'
#     }
#     response = requests.post(f'{BASE_URL}/login', json=payload)
    
#     assert response.status_code == 401
#     assert '无效的用户名或密码' in response.json()['detail']

# def test_admin_register_user():
    # user_data={
    #     "username":"testuser",
    #     "employee_id":"testuser",
    #     "true_name":"testuser",
    #     "gender":"male",
    #     "age":20,
    #     "password":"testuser",
    #     "isSuperAdmin":False
    # }
#     headers = {
#         "Authorization": f"Bearer {auth_token}"
#     }
#     response = requests.post(f'{BASE_URL}/users/register',json=user_data,headers=headers)
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["username"] == user_data["username"]
#     assert response_data["employee_id"] == str(user_data["employee_id"])
#     assert response_data["true_name"] == user_data["true_name"]
#     assert response_data["gender"] == user_data["gender"]
#     assert response_data["age"] == user_data["age"]
#     assert response_data["isSuperAdmin"] == user_data["isSuperAdmin"]
# auth_token2 :str  # 全局变量，用于存储 token
# def test_successful_login2():
#     # 正常登录测试
#     payload = {
#         'username': 'testuser',
#         'password': 'testuser'
#     }
#     response = requests.post(f'{BASE_URL}/login', json=payload)
#     # with open('debug.json', 'a') as f:
#     #     f.write(response.text)
#     # print(response.json())
#     global auth_token2
#     auth_token2=response.json()['access_token']
#     assert response.status_code == 200
#     assert auth_token2 is not None
#     assert response.json()["user_info"]['isSuperAdmin'] == False
    
# def test_update_user_info_valid():
#     """测试正常修改用户信息"""
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     #     user_data={
# #         "username":"testuser",
# #         "employee_id":"testuser",
# #         "true_name":"testuser",
# #         "gender":"male",
# #         "age":20,
# #         "password":"testuser",
# #         "isSuperAdmin":False
# #     }
#     # 构造修改数据
#     update_data = {
#         "true_name": "测试用户新名称",
#         "age": 30,
#         "gender": "female"
#     }
    
#     # 发送修改请求
#     response = requests.patch(
#         f"{BASE_URL}/me",
#         json=update_data,
#         headers=headers
#     )
    
#     # 验证响应
#     assert response.status_code == 200
#     updated_user = response.json()
    
#     # 验证修改字段生效
#     assert updated_user["true_name"] == "admin2"
#     assert updated_user["age"] == 30
#     assert updated_user["gender"] == "female"

# def test_get_current_user_valid_token():
#     """测试带有效token获取用户信息"""
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     response = requests.get(f"{BASE_URL}/me", headers=headers)
    
#     assert response.status_code == 200
#     user_data = response.json()
    
#     # 验证关键字段存在
#     assert all(key in user_data for key in [
#         "username", "employee_id", "true_name", "gender", "age", "isSuperAdmin"
#     ])
#     with open('debug.json', 'a') as f:
#         f.write(f"{user_data}\n")
#         f.flush()
#     # 验证数据一致性（通过已知测试用户数据）
#     assert user_data["username"] == "admin"
#     assert user_data["isSuperAdmin"] is True

# def test_get_all_user_info():
#     """测试获取所有用户信息"""
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     param={
#         "page":1,
#         "page_size":5
#     }
#     response = requests.get(f"{BASE_URL}/users/all", headers=headers,params=param)
#     with open('debug.json', 'a') as f:
#         f.write(f"{response.json()}\n")
#         f.flush()
#     assert response.status_code == 200
#     user_data = response.json()
#     assert user_data["total"] == 2
#     assert len(user_data["items"]) == 2
    
# def test_get_current_user_no_token():
#     """测试未携带token访问"""
#     response = requests.get(f"{BASE_URL}/me")
    
#     assert response.status_code == 401
#     assert "WWW-Authenticate" in response.headers
#     assert "detail" in response.json()
#     assert response.json()["detail"] in ["认证失败","Not authenticated"]

# def test_not_admin_register_user():
#     user_data={
#         "username":"testuser2",
#         "employee_id":"testuser2",
#         "true_name":"testuser2",
#         "gender":"male",
#         "age":20,
#         "password":"testuser2",
#         "isSuperAdmin":False
#     }
#     headers = {
#         "Authorization": f"Bearer {auth_token2}"
#     }
#     response = requests.post(f'{BASE_URL}/users/register',json=user_data,headers=headers)
#     assert response.status_code == 403


# def test_logout():
#     # 登出测试
    
#     headers = {
#         "Authorization": f"Bearer {auth_token}"
#     }
#     response = requests.post(f'{BASE_URL}/logout', headers=headers)
#     with open('debug.json', 'w') as f:
#         f.write(f"{auth_token}\n")
#         f.write(response.text)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()['message']=='注销成功'

# def test_logout2():
#     # 登出测试
    
#     headers = {
#         "Authorization": f"Bearer {auth_token2}"
#     }
#     response = requests.post(f'{BASE_URL}/logout', headers=headers)
#     with open('debug.json', 'w') as f:
#         f.write(f"{auth_token2}\n")
#         f.write(response.text)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()['message']=='注销成功'

# python -m pytest tests/test_auth.py -v -s