"""
@file: urls.py
@brief: users url
@author: feihu1996.cn
@date: 18-7-15 上午2:33
@version: 1.0
"""

from django.conf.urls import url

from users.views import UserInfoView, UserImageUploadView, UserModifyPwdView, SendEmailCodeView, UserModifyEmailView, UserMyCourseView, UserFavOrgView, UserFavTeacherView, UserFavCourseView, UserMessageView

urlpatterns = [
	url(r'^info/$', UserInfoView.as_view(), name='user_info'),  # 用户个人资料url配置
	url(r'^image/upload$', UserImageUploadView.as_view(), name='user_image_upload'),  # 用户图像上传url配置
	url(r'^modify_pwd$', UserModifyPwdView.as_view(), name='user_modify_pwd'),  # 用户修改密码url配置
	url(r'^send_email_code/$', SendEmailCodeView.as_view(), name='user_send_email_code'),  # 发送邮箱验证码url配置
	url(r'^modify_email/$', UserModifyEmailView.as_view(), name='user_modify_email'),  # 用户修改邮箱url配置
	url(r'^my_course/$', UserMyCourseView.as_view(), name='user_my_course'),  # 用户课程url配置
	url(r'^fav/org/$', UserFavOrgView.as_view(), name='user_fav_org'),  # 用户收藏机构url配置
	url(r'^fav/teacher/$', UserFavTeacherView.as_view(), name='user_fav_teacher'),  # 用户收藏讲师url配置
	url(r'^fav/course/$', UserFavCourseView.as_view(), name='user_fav_course'),  # 用户收藏课程url配置
	url(r'^message/$', UserMessageView.as_view(), name='user_message'),  # 用户消息url配置
]
