@echo off
echo 测试后端连接...
echo.
echo 请确保后端服务器正在运行在 http://localhost:8000
echo.
echo 测试连接...
curl -s -o nul -w "HTTP状态码: %%{http_code}\n" http://localhost:8000 2>nul
if %errorlevel% neq 0 (
    echo 无法连接到后端服务器！
    echo 请检查：
    echo 1. 后端服务器是否已启动
    echo 2. 端口8000是否被占用
    echo 3. 防火墙设置
) else (
    echo 后端连接测试完成
)
echo.
echo 现在启动Electron应用...
start "" "build-output\BookDataBaseManager-0.0.0-portable.exe"
echo.
echo 应用已启动！请在开发者工具中查看API请求日志
pause