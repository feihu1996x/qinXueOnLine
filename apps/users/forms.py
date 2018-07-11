"""
@file: forms.py
@brief: 用户提交表单自动验证
@author: feihu1996.cn
@date: 18-7-11 下午3:01
@version: 1.0
"""

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
	"""
	用户登录表单验证
	"""
	# required=True则表明该字段为必填字段
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
	"""
	用户注册表单验证
	"""
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, min_length=5)
	# 验证码字段验证
	# 使用error_messages参数可以自定义异常响应
	captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
	"""
	找回密码表单验证
	"""
	email = forms.EmailField(required=True)
	captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ResetPwdForm(forms.Form):
	"""
	重置密码表单验证
	"""
	password = forms.CharField(required=True, min_length=5)
	password1 = forms.CharField(required=True, min_length=5)
	email = forms.EmailField(required=True)
