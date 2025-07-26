# Vue项目打包为Electron桌面应用说明

## 构建步骤

### 方法一：使用批处理脚本（推荐）
直接双击运行 `build-exe.bat` 文件，脚本会自动完成以下步骤：
1. 构建Vue项目
2. 打包Electron应用
3. 生成exe文件

### 方法二：手动命令行构建
```bash
# 1. 构建Vue项目
npm run build

# 2. 打包Electron应用
npm run electron:build
```

## 开发模式
如果需要在开发模式下运行Electron应用：
- 双击运行 `dev-electron.bat`
- 或者命令行运行：`npm run electron:dev`

## 生成的文件
构建完成后，在 `build-output` 目录下会生成：

- `BookDataBaseManager-0.0.0-x64.exe` - Windows安装版
  - 需要安装到系统中
  - 会创建桌面快捷方式和开始菜单项
  
- `BookDataBaseManager-0.0.0-portable.exe` - 便携版
  - 无需安装，直接运行
  - 适合在不同电脑间移动使用

## 项目结构
- `main.js` - Electron主进程文件
- `electron-builder.yml` - 打包配置文件
- `dist/` - Vue构建输出目录
- `build-output/` - Electron打包输出目录

## 测试应用
运行 `test-app.bat` 可以快速启动便携版应用进行测试。

## 故障排除

### 资源加载错误
如果遇到资源加载错误（如CSS或JS文件404错误）：
1. 确保vite.config.js中的base设置为相对路径：`base: './`
2. 重新构建：`npm run build`
3. 重新打包：`npm run electron:build`

### Vue应用不显示
如果应用只显示背景但没有Vue内容：
1. 检查路由配置是否使用Hash模式：`createWebHashHistory()`
2. 检查控制台是否有JavaScript错误
3. 确认Vue应用是否正确挂载到#app元素

### 后端连接问题
如果应用无法向后端发送请求：
1. 确保后端服务器正在运行在 `http://localhost:8000`
2. 检查防火墙设置，确保端口8000可访问
3. 运行 `test-backend.bat` 测试后端连接
4. 在开发者工具中查看API请求日志

### API配置说明
- **开发环境**：使用Vite代理 `/api` -> `http://localhost:8000`
- **Electron环境**：直接连接 `http://localhost:8000`
- **环境检测**：自动检测是否在Electron中运行

### 最新修复的问题
- ✅ 资源路径问题（CSS/JS文件404错误）
- ✅ 路由模式改为Hash模式（适合Electron环境）
- ✅ 修复了API配置导入错误（`isElectron is not a function`）
- ✅ 修复了后端连接检测的405错误（改用GET请求）
- ✅ 简化了环境检测逻辑，避免复杂的模块导入
- ✅ 移除了自动打开的开发者工具（用户体验优化）
- ✅ 添加了可选的调试模式

### 使用工具
- `test-app.bat` - 启动应用
- `diagnose.bat` - 全面的问题诊断脚本
- `enable-debug.bat` - 启用调试模式
- `test-backend.bat` - 后端连接测试脚本

### 调试模式
默认情况下，应用不会显示详细的调试日志。如需调试：
1. 按F12打开开发者工具
2. 在Console中输入：`localStorage.setItem('debug', 'true')`
3. 刷新页面即可看到详细的API日志
4. 关闭调试：`localStorage.removeItem('debug')`

## 注意事项
1. 确保已安装所有依赖：`npm install`
2. 构建前会自动重新构建Vue项目
3. 如果构建失败，请检查Node.js和npm版本
4. 图标文件位于 `public/booklogo.png`
5. 资源路径必须使用相对路径才能在Electron中正确加载