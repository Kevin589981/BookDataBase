@echo off
echo 开始构建Vue项目...
call npm run build

echo 检查构建结果...
if not exist "dist\index.html" (
    echo 构建失败！请检查错误信息。
    pause
    exit /b 1
)

echo Vue项目构建成功！
echo 开始打包Electron应用...
call npm run electron:build

echo 构建完成！
echo 可执行文件位置: build-output\
echo.
echo 生成的文件:
echo - BookDataBaseManager-0.0.0-x64.exe (安装版)
echo - BookDataBaseManager-0.0.0-portable.exe (便携版)
echo.
pause