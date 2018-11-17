# qinXueOnLine

> 仿"中国大学MOOC"

## Tech Stack

- HTML/CSS/JavaScript
- JQuery
- Python/Django/Xadmin/urllib
- MySQL
- Docker
- Supervisor
- Nginx
- Gunicorn
- Selenium
- Redis

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

## Demo Link
[http://dev.feihu1996.cn/qinXueOnLine/](http://dev.feihu1996.cn/qinXueOnLine/ "qinXueOnLine")
