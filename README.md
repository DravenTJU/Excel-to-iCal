# Excel-to-iCal 排班表转换工具

这是一个基于Django的Web应用程序，用于将Excel格式的排班表自动转换为iCal日历文件。特别适用于需要将工作排班表导入到日历应用的场景。

## 功能特点

- 支持Excel格式(.xlsx, .xls)的排班表上传
- 自动识别并提取排班信息
- 生成标准iCal格式的日历文件
- 支持时区设置（默认为太平洋/奥克兰时区）
- Web界面操作，简单直观
- 支持跨域请求

## 技术栈

- Python 3.x
- Django 4.2.7
- Django REST framework 3.14.0
- pandas 2.1.3
- icalendar 5.0.11
- 其他依赖见 requirements.txt

## 安装说明

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

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 初始化数据库
```bash
cd backend
python manage.py migrate
```

5. 启动开发服务器
```bash
python manage.py runserver
```

## 使用方法

1. 访问 `http://localhost:8000/api/convert/` 
2. 上传Excel格式的排班表
3. 系统会自动处理并生成iCal文件
4. 点击下载链接获取生成的iCal文件
5. 将iCal文件导入到你的日历应用中

## Excel文件格式要求

排班表需要符合以下格式：
- 包含周信息（[WEEK XX] 格式）
- 每天的日期信息（格式如：Monday 11/11）
- 包含员工名称和对应的排班时间
- 时间格式应为标准的24小时制（如：09:00-17:00）

## API接口

- `POST /api/convert/`: 上传Excel文件并转换
- `GET /api/download/<filename>/`: 下载生成的iCal文件

## 注意事项

- 默认时区设置为太平洋/奥克兰时区，可在代码中修改
- 上传文件大小限制为5MB
- 建议在生产环境中修改Django的SECRET_KEY和DEBUG设置
- 生产环境部署时请适当配置CORS和安全设置

## 许可证

[MIT License](LICENSE)

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

## 作者

Draven

## 致谢

感谢所有为这个项目做出贡献的开发者。
