"""
@file: send_email.py
@brief: send email
@author: feihu1996.cn
@date: 18-7-11 下午6:49
@version: 1.0
"""
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from utils.random_key import RandomKey
from qinXueOnLine.settings import EMAIL_FROM


def send_email(email, send_type='register'):
	"""
	;向用户发送验证邮件
	:param email, send_type:
	:return:
	"""
	email_record_model = EmailVerifyRecord()
	code = RandomKey(length=16, has_symbol=False).generate()['data']
	email_record_model.code = code
	email_record_model.email = email
	email_record_model.send_type = send_type
	# 将验证信息先保存到数据库中
	email_record_model.save()

	# 发送邮件
	email_title = ''
	email_body = ''

	if send_type == 'register':
		email_title = '勤学在线网注册激活链接'
		email_body = '请点击链接激活您的帐号: http://127.0.0.1:8000/active/{0}'.format(code)
	elif send_type == 'forget':
		email_title = '勤学在线网密码重置链接'
		email_body = '请点击链接重置您的密码: http://127.0.0.1:8000/resetpwd/{0}'.format(code)

	send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
	if send_status:
		pass
