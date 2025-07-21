@echo off
chcp 936 >nul 2>&1  :: 设置代码页为GBK
title 启动项目服务

:: 获取脚本所在目录（即DataBase文件夹）
set "BASE_DIR=%~dp0"
:: 去除路径末尾的反斜杠（如果有）
if "%BASE_DIR:~-1%"=="\" set "BASE_DIR=%BASE_DIR:~0,-1%"

:: 设置其他路径（相对于BASE_DIR）
set "CONDA_ENV=%BASE_DIR%\.conda"
set "SERVER_DIR=%BASE_DIR%\server"
set "FRONTEND_DIR=%BASE_DIR%\frontend"

:: 检查必要的目录是否存在
if not exist "%SERVER_DIR%" (
    echo 错误：找不到server目录
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%" (
    echo 错误：找不到frontend目录
    pause
    exit /b 1
)

:: 启动后端服务
echo 正在启动后端服务...
start "后端服务" cmd /k "chcp 936 >nul 2>&1 & cd /d "%BASE_DIR%" & conda activate "%CONDA_ENV%" & timeout /t 2 >nul & uvicorn server.main:app --reload"

:: 等待2秒确保后端启动
timeout /t 2 >nul

:: 启动前端服务
echo 正在启动前端服务...
start "前端服务" cmd /k "chcp 936 >nul 2>&1 & cd /d "%FRONTEND_DIR%" & npm run dev"

timeout /t 2 >nul

echo 后端和前端服务已启动，请勿关闭这两个命令行窗口
echo 前端开发服务器通常运行在: http://localhost:5173
echo 如果使用打包版本，请访问: http://localhost:4173
echo.
echo 注意：DataBase文件夹当前位于: %BASE_DIR%
pause