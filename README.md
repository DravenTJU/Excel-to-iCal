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
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装后端依赖
```bash
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

## 生产环境部署（Debian 12 + NGINX）

### 1. 系统准备

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装必要的包
sudo apt install -y python3-pip python3-venv nginx supervisor git
```

### 2. 克隆项目

```bash
# 创建项目目录
sudo mkdir -p /var/www
sudo chown -R $USER:$USER /var/www

# 克隆项目
cd /var/www
git clone https://github.com/yourusername/Excel-to-iCal.git
cd Excel-to-iCal
```

### 3. 后端部署

```bash
# 创建虚拟环境
cd backend
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn  # 生产环境 WSGI 服务器

# 收集静态文件
python manage.py collectstatic --noinput

# 创建 media 目录
mkdir -p media
chmod 755 media
```

#### 配置 Supervisor

创建 supervisor 配置文件：
```bash
sudo nano /etc/supervisor/conf.d/excel-to-ical.conf
```

添加以下内容：
```ini
[program:excel-to-ical]  # 程序名称，用于标识这个进程
directory=/var/www/Excel-to-iCal/backend  # 工作目录
command=/var/www/Excel-to-iCal/venv/bin/gunicorn config.wsgi:application --workers 3 --bind 127.0.0.1:8000  # 启动命令
user=www-data  # 运行进程的用户
autostart=true  # 随 supervisor 启动自动启动
autorestart=true  # 进程崩溃时自动重启
stderr_logfile=/var/log/excel-to-ical.err.log  # 错误日志位置
stdout_logfile=/var/log/excel-to-ical.out.log  # 标准输出日志位置
```

启动服务：
```bash
# 重新加载配置文件
sudo supervisorctl reread
# 更新配置
sudo supervisorctl update
# 启动服务
sudo supervisorctl start excel-to-ical
# 停止服务
sudo supervisorctl stop excel-to-ical
# 重启服务
sudo supervisorctl restart excel-to-ical
# 查看所有程序状态
sudo supervisorctl status
```

### 4. 前端部署

```bash
# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 构建前端
cd /var/www/Excel-to-iCal/frontend
npm install
npm run build
```

### 5. NGINX 配置

创建 NGINX 配置文件：
```bash
sudo nano /etc/nginx/sites-available/excel-to-ical
```

添加以下内容：
```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名

    # 前端静态文件
    location / {
        root /var/www/Excel-to-iCal/frontend/build;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 媒体文件
    location /media/ {
        alias /var/www/Excel-to-iCal/backend/media/;
    }
}
```

启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/excel-to-ical /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

### 6. 环境变量配置

创建 .env 文件：
```bash
# 后端 .env
cd /var/www/Excel-to-iCal/backend
nano .env
```

添加以下内容：
```env
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=your_domain.com,www.your_domain.com
CORS_ALLOWED_ORIGINS=https://your_domain.com
```

### 7. 安全设置

```bash
# 设置文件权限
sudo chown -R www-data:www-data /var/www/Excel-to-iCal
sudo chmod -R 755 /var/www/Excel-to-iCal

# 配置防火墙
sudo apt install -y ufw
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

### 8. SSL 配置（Cloudflare 源服务器证书）

1. 在 Cloudflare 面板中生成源服务器证书：
   - 登录 Cloudflare 控制面板
   - 进入你的域名设置
   - 点击 "SSL/TLS" > "Origin Server"
   - 点击 "Create Certificate"
   - 选择证书有效期（建议 15 年）
   - 生成证书，你会得到两个文件：
     - Origin Certificate (证书文件)
     - Private Key (私钥文件)

2. 在服务器上配置证书：
```bash
# 创建证书目录
sudo mkdir -p /etc/nginx/ssl
cd /etc/nginx/ssl

# 创建证书和私钥文件
sudo nano excel-to-ical.pem  # 粘贴 Origin Certificate 内容
sudo nano excel-to-ical.key  # 粘贴 Private Key 内容

# 设置适当的权限
sudo chmod 644 excel-to-ical.pem
sudo chmod 600 excel-to-ical.key
```

3. 修改 NGINX 配置：
```bash
sudo nano /etc/nginx/sites-available/excel-to-ical
```

```nginx
# HTTP - 将所有 HTTP 流量重定向到 HTTPS
server {
    listen 80;
    server_name your_domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS - 主配置
server {
    listen 443 ssl http2;
    server_name your_domain.com;

    # SSL 配置
    ssl_certificate /etc/nginx/ssl/excel-to-ical.pem;
    ssl_certificate_key /etc/nginx/ssl/excel-to-ical.key;
    
    # SSL 优化
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    
    # 现代 SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # HSTS (如果你确定只使用 HTTPS)
    add_header Strict-Transport-Security "max-age=63072000" always;

    # 客户端缓存设置
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires max;
        log_not_found off;
        access_log off;
        add_header Cache-Control "public, no-transform";
    }
    
    # 前端静态文件
    location / {
        root /var/www/Excel-to-iCal/frontend/build;
        index index.html;
        try_files $uri $uri/ /index.html;

        # 禁用缓存 index.html
        location = /index.html {
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            expires 0;
        }
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 增加超时时间
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 媒体文件
    location /media/ {
        alias /var/www/Excel-to-iCal/backend/media/;
        expires 1h;
        add_header Cache-Control "public, no-transform";
    }

    # 禁止访问 . 文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

4. 验证并重启 NGINX：
```bash
sudo nginx -t
sudo systemctl restart nginx
```

5. 在 Cloudflare 中配置：
   - SSL/TLS 加密模式设置为 "Full (strict)"
   - 确保域名已经启用了 Cloudflare 代理（橙色云朵）
   - 创建以下 DNS 记录：
     ```
     Type  Name  Content          Proxy status
     A     @     你的服务器IP     Proxied
     ```

### 安全注意事项

1. 证书和私钥安全：
```bash
# 定期备份证书和私钥
sudo cp /etc/nginx/ssl/excel-to-ical.* /path/to/backup/

# 确保权限正确
sudo chown root:root /etc/nginx/ssl/excel-to-ical.*
sudo chmod 644 /etc/nginx/ssl/excel-to-ical.pem
sudo chmod 600 /etc/nginx/ssl/excel-to-ical.key
```

2. 监控证书有效期：
```bash
# 创建证书检查脚本
sudo nano /usr/local/bin/check-ssl-cert.sh
```

```bash
#!/bin/bash
CERT_FILE="/etc/nginx/ssl/excel-to-ical.pem"
DAYS=30

exp_date=$(openssl x509 -enddate -noout -in "$CERT_FILE" | cut -d= -f2)
exp_epoch=$(date -d "$exp_date" +%s)
now_epoch=$(date +%s)
days_left=$(( (exp_epoch - now_epoch) / 86400 ))

if [ $days_left -le $DAYS ]; then
    echo "警告：SSL证书将在 $days_left 天后过期"
    # 可以添加发送邮件通知的命令
fi
```

```bash
# 设置执行权限
sudo chmod +x /usr/local/bin/check-ssl-cert.sh

# 添加到 crontab
sudo crontab -e
# 添加以下行（每周检查一次）
0 0 * * 0 /usr/local/bin/check-ssl-cert.sh
```

### 9. 维护命令

```bash
# 重启服务
sudo supervisorctl restart excel-to-ical
sudo systemctl restart nginx

# 查看日志
sudo tail -f /var/log/excel-to-ical.err.log
sudo tail -f /var/log/excel-to-ical.out.log
sudo tail -f /var/log/nginx/error.log

# 清理临时文件
find /var/www/Excel-to-iCal/backend/media -mtime +7 -type f -delete
```

### 10. 注意事项

- 确保域名已正确解析到服务器 IP
- 定期备份数据和配置文件
- 定期更新系统和依赖包
- 监控服务器资源使用情况
- 配置日志轮转以防止日志文件过大
- 设置定时任务清理过期的临时文件

## 故障排除

1. 如果服务无法启动：
```bash
sudo supervisorctl status
sudo journalctl -u nginx
```

2. 如果静态文件无法访问：
```bash
sudo nginx -t
sudo chown -R www-data:www-data /var/www/Excel-to-iCal/frontend/build
```

3. 如果上传失败：
```bash
sudo chown -R www-data:www-data /var/www/Excel-to-iCal/backend/media
sudo chmod 755 /var/www/Excel-to-iCal/backend/media
```
