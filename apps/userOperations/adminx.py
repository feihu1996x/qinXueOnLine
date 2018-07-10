"""
@file: adminx.py
@brief: 
@author: feihu1996.cn
@date: 18-7-10 下午4:36
@version: 1.0
"""

import xadmin

from userOperations.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskAdmin:
    list_display = ['user_name', 'cell_phone_number', 'course_name', 'add_time']
    search_fields = ['user_name', 'cell_phone_number', 'course_name']
    list_filter = ['user_name', 'cell_phone_number', 'course_name', 'add_time']


class CourseCommentsAdmin:
    list_display = ['user', 'course', 'comment_content', 'add_time']
    search_fields = ['user', 'course', 'comment_content']
    list_filter = ['user__username', 'course__name', 'comment_content', 'add_time']


class UserFavoriteAdmin:
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user__username', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin:
    list_display = ['user', 'message_content', 'has_read', 'add_time']
    search_fields = ['user', 'message_content', 'has_read']
    list_filter =list_display


class UserCourseAdmin:
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user__username', 'course__name', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)

