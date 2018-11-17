# qinXueOnLine

## 项目描述

仿"中国大学MOOC"

## 技术栈

HTML
CSS
JavaScript
JQuery
Django(Web后端服务)
Xadmin(后台管理系统)
MySQL
Docker(容器端口映射)
Supervisor(进程管理)
Nginx(反向代理)
Gunicorn(WSGI)
urllib
Selenium
多线程
Redis

## Build and Setup

```bash

# 安装依赖
yum install mysql-devel gcc gcc-devel python-devel -y
pip install -r requirements.txt

# 导入数据库
mysql -uroot -p qinXueOnLine < qinXueOnLine.sql

# 启动Web App
python3 begin.py

```

