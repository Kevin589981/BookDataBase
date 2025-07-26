@echo off
echo 🔍 Electron应用问题诊断
echo ========================
echo.

echo 1. 检查构建文件...
if exist "build-output\BookDataBaseManager-0.0.0-portable.exe" (
    echo ✅ 便携版exe文件存在
) else (
    echo ❌ 便携版exe文件不存在，请运行: npm run electron:build
    goto :end
)

echo.
echo 2. 检查后端连接...
curl -s -o nul -w "HTTP状态码: %%{http_code}\n" http://localhost:8000 2>nul
if %errorlevel% neq 0 (
    echo ❌ 无法连接到后端服务器 http://localhost:8000
    echo    请确保后端服务器已启动
) else (
    echo ✅ 后端服务器连接正常
)

echo.
echo 3. 检查端口占用...
netstat -an | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo ✅ 端口8000有服务监听
    netstat -an | findstr :8000
) else (
    echo ❌ 端口8000没有服务监听
)

echo.
echo 4. 检查关键文件...
if exist "src\utils\api.js" (
    echo ✅ API配置文件存在
) else (
    echo ❌ API配置文件缺失
)

if exist "dist\index.html" (
    echo ✅ 构建输出文件存在
) else (
    echo ❌ 构建输出文件缺失，请运行: npm run build
)

echo.
echo 5. 诊断完成
echo.
echo 如果所有检查都通过，请运行 test-app.bat 启动应用
echo 如果有问题，请根据上述提示进行修复

:end
echo.
pause