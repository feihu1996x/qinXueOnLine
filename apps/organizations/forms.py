"""
@file: forms.py
@brief: 表单字段验证
@author: feihu1996.cn
@date: 18-7-12 下午7:47
@version: 1.0
"""
import re

from django import forms

from userOperations.models import UserAsk


# class UserAskForm(forms.Form):
# 	user_name = forms.CharField(required=True, min_length=2, max_length=20)
# 	cell_phone_number = forms.CharField(required=True, min_length=11, max_length=11)
# 	course_name = forms.CharField(required=True, min_length=5)


class UserAskModelForm(forms.ModelForm):
	"""
	用于替换普通Form的ModelForm,
	它既是Form，又是Model
	"""
	# new_field = forms.CharField(required=True, min_length=10)
	pass

	class Meta:
		# 指定要转换成ModelForm的Model
		model = UserAsk

		# 指定要对Model中的哪些字段进行验证
		# 在定义Model时的一些字段约束也会被继承
		fields = ['user_name', 'cell_phone_number', 'course_name']

	def clean_cell_phone_number(self):
		"""
		自定义表单字段验证函数,
		正则表达式匹配手机号码
		:return:
		"""
		cell_phone_number = self.cleaned_data['cell_phone_number']
		cell_phone_number_pattern = re.compile('^1[358]\d{9}$|^147\d{8}$|^176\d{8}$')
		if cell_phone_number_pattern.match(cell_phone_number):
			return cell_phone_number
		else:
			raise forms.ValidationError(u"手机号码不合法", code="mobile_invalid")
