from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auto_login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from users.models import UserProfile, EmailVerifyRecord
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm
from utils.send_email import send_email


class CustomBackend(ModelBackend):
	"""
	重载authenticate用户认证函数
	"""
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			# 根据username查询user
			# 这里传进来的username参数既可以是用户名也可以是邮箱地址
			# 通过Q类，实现字段的或查询
			# 进而实现了通过用户名和邮箱都能登录
			user_model = UserProfile.objects.get(Q(username=username)|Q(email=username))
			# 校验密码
			if user_model.check_password(password):
				return user_model
		except:
			return None


# Create your views here.
# def login(request):
# 	"""
# 	:用户登录请求处理函数(建议用类来处理用户请求)
# 	:param request:
# 	:return:
# 	"""
# 	if request.method == 'POST':
# 		username = request.POST.get('username', '')
# 		password = request.POST.get('password', '')
# 		user_model = authenticate(username=username, password=password)
# 		if user_model is not None:
# 			# 用户登录认证通过
# 			auto_login(request, user_model)
# 			return render(request, 'index.html')
# 		else:
# 			# 用户登录认证未通过
# 			return render(request, 'login.html', {'msg': '用户名或密码错误'})
# 	elif request.method == 'GET':
# 		return render(request, 'login.html', {})


class LoginView(View):
	"""
	用户登录请求处理类
	"""
	def get(self, request):
		"""
		:如果是get请求
		:param request:
		:return:
		"""
		return render(request, 'login.html', {})

	def post(self, request):
		"""
		；如果是post请求
		:param request:
		:return:
		"""
		login_form = LoginForm(request.POST)
		if login_form.is_valid():  # 用户登录提交表单字段验证成功
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			user_model = authenticate(username=username, password=password)
			if user_model is not None:  # 用户登录认证通过
				if user_model.is_active:  # 用户已经激活
					auto_login(request, user_model)
					return render(request, 'index.html')
				else:  # 用户未激活
					return render(request, 'login.html', {'msg': '用户尚未激活！', 'login_form': login_form})
			else:  # 用户登录认证未通过
				return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
		else:
			# 用户登录提交表单字段验证失败
			return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
	"""
	用户注册请求处理类
	"""
	def get(self, request):
		register_form = RegisterForm()
		return render(request, 'register.html', {'register_form': register_form})

	def post(self, request):
		register_form = RegisterForm(request.POST)

		if register_form.is_valid():  # 用户注册提交表单字段验证成功
			email = request.POST.get('email', '')
			password = request.POST.get('password', '')

			try:
				UserProfile.objects.get(Q(username=email)|Q(email=email))  # 查询当前注册用户是否已经存在
			except:  # 将用户注册信息写入数据库
				user_model = UserProfile()
				user_model.username = email
				user_model.email = email
				user_model.password = make_password(password=password)
				user_model.is_active = False # 用户尚未激活
				user_model.save()
				send_email(email)  # 发送注册激活链接
				return render(request, 'login.html', {'msg': '注册激活链接已经发送到您的邮箱'})
			else:
				return render(request, 'register.html', {'msg': '用户已经存在！', 'register_form': register_form})

		else:  # 用户注册提交表单字段验证失败
			return render(request, 'register.html', {'register_form': register_form})


class ActiveView(View):
	"""
	用户激活请求处理类
	"""
	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			for record in all_records:
				email = record.email
				user = UserProfile.objects.get(email=email)
				user.is_active = True
				user.save()
			return render(request, 'login.html', {'msg': '用户已经激活，请登录！'})
		else:
			return render(request, 'active_fail.html', {'msg': '激活链接失效！'})


class ForgetPwdView(View):
	"""
	找回密码请求处理类
	"""
	def get(self, request):
		forget_pwd_form = ForgetPwdForm()
		return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form})

	def post(self, request):
		forget_pwd_form = ForgetPwdForm(request.POST)

		if forget_pwd_form.is_valid():  # 找回密码表单字段验证成功
			email = request.POST.get('email', '')
			send_email(email=email, send_type='forget') # 发送找回密码链接
			return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form, 'msg': '重置密码链接已经发送到您的邮箱！'})
		else:
			return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form})


class ResetPwdView(View):
	"""
	重置密码请求处理类
	"""
	def get(self, request, reset_code):
		all_records = EmailVerifyRecord.objects.filter(code=reset_code)
		if all_records:
			for record in all_records:
				email = record.email
				return render(request, 'password_reset.html', {'email': email})
		else:
			return render(request, 'password_reset.html', {'msg': '链接失效！'})

	def post(self, request, reset_code):
		reset_pwd_form = ResetPwdForm(request.POST)
		if reset_pwd_form.is_valid():
			password = request.POST.get('password', '')
			re_password = request.POST.get('password1', '')
			email = request.POST.get('email', '')

			if password != re_password:  # 两次密码输入不一致
				return render(request, 'password_reset.html', {'email': email, 'reset_pwd_form': reset_pwd_form, 'msg': '两次密码不一致，请重新输入'})
			else: # 保存新密码
				user_model = UserProfile.objects.get(email=email)
				user_model.password = make_password(password=password)
				user_model.save()
				return render(request, 'login.html', {'msg': '密码重置成功，请重新登录'})
		else:
			return render(request, 'password_reset.html', {'email': reset_pwd_form.data.get('email'), 'reset_pwd_form': reset_pwd_form})
