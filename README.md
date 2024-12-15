# Excel-to-iCal 排班表转换工具

这是一个基于 Django 和 React 的 Web 应用程序，用于将 Excel 格式的排班表自动转换为 iCal 日历文件。特别适用于需要将工作排班表导入到日历应用的场景。

## 功能特点

- 支持 Excel 格式(.xlsx, .xls)的排班表上传
- 自动识别并提取排班信息
- 生成标准 iCal 格式的日历文件
- 支持时区设置（默认为太平洋/奥克兰时区）
- 美观的 Web 界面，简单直观
- 支持多语言（英文、中文、日语）
- 响应式设计，支持移动端
- 优雅的动画效果和交互体验

## 界面特点

- 简洁现代的设计风格
- 实时语言切换功能
- 文件上传状态实时反馈
- 转换成功后的动画提示
- 清晰的操作指引
- 适配移动端的响应式布局

## 技术栈

### 后端
- Python 3.x
- Django 4.2.7
- Django REST framework 3.14.0
- pandas 2.1.3
- icalendar 5.0.11
- 其他依赖见 requirements.txt

### 前端
- React 18
- TypeScript
- Ant Design 5.x
- Axios
- 其他依赖见 frontend/package.json

## 安装说明

### 后端安装
1. 克隆仓库
```bash
git clone https://github.com/yourusername/Excel-to-iCal.git
cd Excel-to-iCal
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

4. 初始化数据库
```bash
python manage.py migrate
```

### 前端安装
1. 安装前端依赖
```bash
cd frontend
npm install
```

## 启动服务

1. 启动后端服务器
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

2. 启动前端开发服务器
```bash
cd frontend
npm start
```

## 使用方法

1. 访问 `http://localhost:3000` 
2. 选择界面语言（支持英文、中文、日语）
3. 上传 Excel 格式的排班表
4. 等待系统自动处理并生成 iCal 文件
5. 点击下载按钮获取生成的 iCal 文件
6. 将 iCal 文件导入到你的日历应用中

## Excel 文件格式要求

排班表需要符合以下格式：
- 包含周信息（[WEEK XX] 格式）
- 每天的日期信息（格式如：Monday 11/11）
- 包含员工名称和对应的排班时间
- 时间格式应为标准的24小时制（如：09:00-17:00）

## API 接口

- `POST /api/convert/`: 上传 Excel 文件并转换
- `GET /api/download/<filename>/`: 下载生成的 iCal 文件

## 开发环境配置

### 后端配置
- 默认时区设置为太平洋/奥克兰时区，可在代码中修改
- 上传文件大小限制为 5MB
- 开发环境已配置 CORS，支持跨域请求
- 建议在生产环境中修改 Django 的 SECRET_KEY 和 DEBUG 设置

### 前端配置
- 默认后端 API 地址为 `http://192.168.1.122:8000`
- 可通过环境变量 `REACT_APP_API_URL` 修改 API 地址
- 支持 TypeScript 类型检查
- 使用 Ant Design 组件库
- 支持多语言国际化

## 界面交互特点

- 文件上传状态实时反馈
- 转换成功后的动画效果
- 自动检测浏览器语言
- 响应式布局适配各种屏幕尺寸
- 优雅的错误处理和提示

## 注意事项

- 生产环境部署时请修改相应的安全设置
- 确保上传文件的格式正确
- 建议定期清理 media 目录中的临时文件
- 前后端跨域配置需要根据实际部署环境调整

## 许可证

[MIT License](LICENSE)

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 作者

Draven

## 致谢

感谢所有为这个项目做出贡献的开发者。
