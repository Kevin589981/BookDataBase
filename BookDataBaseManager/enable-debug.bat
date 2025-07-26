@echo off
echo 启用调试模式...
echo.
echo 这将在应用中启用详细的调试日志
echo 包括：
echo - API请求/响应日志
echo - 环境检测信息
echo - 后端连接状态
echo.
echo 启动应用后，在开发者工具的Console中输入：
echo localStorage.setItem('debug', 'true')
echo.
echo 然后刷新页面即可看到详细日志
echo.
echo 要关闭调试模式，输入：
echo localStorage.removeItem('debug')
echo.
start "" "build-output\BookDataBaseManager-0.0.0-portable.exe"
echo 应用已启动！按F12打开开发者工具
pause