@echo off
echo 启动图书管理系统...
echo.
echo 最新修复内容：
echo 1. ? 修复了资源路径问题（使用相对路径）
echo 2. ? 修改路由为Hash模式（更适合Electron）
echo 3. ? 修复了API配置导入问题
echo 4. ? 修复了后端连接检测（避免405错误）
echo 5. ? 移除了自动打开的开发者工具
echo.
echo 请确保后端服务器运行在 http://localhost:8000
echo.
start "" "build-output\BookDataBaseManager-0.0.0-portable.exe"
echo 应用已启动！
echo.
echo 如需调试：
echo - 按F12打开开发者工具
echo - 或运行 enable-debug.bat 启用详细日志
echo.
pause