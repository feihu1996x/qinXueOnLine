"""
@file: mixin_utils.py
@brief: mixin utils
@author: feihu1996.cn
@date: 18-7-13 下午11:17
@version: 1.0
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin:
	"""
	拦截未登录的请求
	"""
	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
