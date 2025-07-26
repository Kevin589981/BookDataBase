# Electron应用使用指南

## 🚀 快速开始

### 1. 启动后端服务器
在使用Electron应用之前，请确保后端服务器正在运行：
```bash
# 启动你的后端服务器（端口8000）
# 例如：python manage.py runserver 0.0.0.0:8000
```

### 2. 测试后端连接
运行测试脚本检查后端是否可用：
```bash
# 双击运行
test-backend.bat
```

### 3. 启动Electron应用
```bash
# 方式1：使用便携版（推荐）
build-output\BookDataBaseManager-0.0.0-portable.exe

# 方式2：使用安装版
build-output\BookDataBaseManager-0.0.0-x64.exe
```

## 🔧 配置说明

### API配置
- **后端地址**: `http://localhost:8000`
- **超时时间**: 10秒
- **环境检测**: 自动检测Electron环境

### 网络配置
- **开发环境**: 使用Vite代理 `/api` → `http://localhost:8000`
- **Electron环境**: 直接连接 `http://localhost:8000`
- **CORS**: 已禁用webSecurity以支持跨域请求

## 🐛 故障排除

### 后端连接问题
如果看到"后端服务器连接失败"错误：

1. **检查后端服务器状态**
   ```bash
   curl http://localhost:8000
   ```

2. **检查端口占用**
   ```bash
   netstat -an | findstr :8000
   ```

3. **检查防火墙设置**
   - 确保Windows防火墙允许端口8000
   - 确保杀毒软件没有阻止连接

4. **查看详细错误信息**
   - 打开开发者工具（F12）
   - 查看Console标签页的错误信息
   - 查看Network标签页的请求状态

### 常见错误及解决方案

#### 错误：`net::ERR_CONNECTION_REFUSED`
**原因**: 后端服务器未启动或端口不正确
**解决**: 启动后端服务器并确认端口为8000

#### 错误：`net::ERR_NETWORK_ACCESS_DENIED`
**原因**: 防火墙或安全软件阻止了连接
**解决**: 检查防火墙设置，允许应用访问网络

#### 错误：`Request timeout`
**原因**: 网络连接超时
**解决**: 检查网络连接，或增加超时时间

## 📊 调试信息

应用启动时会在控制台显示以下调试信息：
- 环境检测结果
- API配置信息
- 后端连接状态
- 请求/响应日志

## 🔍 开发者工具

Electron应用会自动打开开发者工具，你可以：
- 查看控制台日志
- 监控网络请求
- 调试Vue应用
- 检查应用状态

## 📝 配置文件

### 主要配置文件
- `src/config/index.js` - 应用配置
- `src/utils/api.js` - API配置
- `main.js` - Electron主进程配置
- `vite.config.js` - 构建配置

### 修改后端地址
如需修改后端地址，编辑 `src/config/index.js`：
```javascript
export const API_CONFIG = {
  BACKEND_URL: 'http://your-backend-url:port',
  // ...
}
```

然后重新构建应用：
```bash
npm run electron:build
```

## 🎯 使用建议

1. **首次使用**: 运行 `test-backend.bat` 确认环境配置
2. **开发调试**: 使用开发者工具监控API请求
3. **生产使用**: 使用便携版，无需安装
4. **问题反馈**: 保存控制台日志以便问题诊断

## 📞 技术支持

如遇到问题，请提供：
- 错误截图
- 控制台日志
- 后端服务器状态
- 操作系统版本