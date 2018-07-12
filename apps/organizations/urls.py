"""
@file: urls.py
@brief: organazitions url
@author: feihu1996.cn
@date: 18-7-12 下午8:13
@version: 1.0
"""

from django.conf.urls import url

from organizations.views import OrgListView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView

urlpatterns = [
	url(r'^list/$', OrgListView.as_view(), name='org_list'),  # 课程机构列表url配置
	url(r'^user_ask/$', UserAskView.as_view(), name='user_ask'),  # 用户咨询url配置
	url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(),  name='org_home'),  # 机构首页url配置
	url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(),  name='org_course'),  # 机构课程url配置
	url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(),  name='org_desc'),  # 机构详情url配置
	url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(),  name='org_teacher'),  # 机构讲师url配置
	url(r'^user_fav/$', AddFavView.as_view(),  name='user_fav'),  # 用户收藏/取消收藏url配置
]
