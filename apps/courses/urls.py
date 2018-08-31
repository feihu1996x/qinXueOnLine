"""
@file: urls.py
@brief: courses url
@author: feihu1996.cn
@date: 18-7-12 下午8:13
@version: 1.0
"""

from django.conf.urls import url

from courses.views import CourseListView, CourseDetailView, CourseChapterView, CourseCommentView, CoursePlayView

urlpatterns = [
	url(r'^list/$', CourseListView.as_view(), name='course_list'),  # 课程列表url配置
	url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),  # 课程详情url配置
	url(r'^chapter/(?P<course_id>\d+)/$', CourseChapterView.as_view(), name='course_chapter'),  # 课程章节url配置
	url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),  # 课程评论url配置
	url(r'^play/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name='course_play'),  # 课程视频播放url配置
]
