"""
@file: adminx.py
@brief: 
@author: feihu1996.cn
@date: 18-7-10 下午3:44
@version: 1.0
"""

import xadmin

from courses.models import Course, Chapter, Video, CourseResource


class CourseAdmin:
    list_display = ['name', 'desc', 'detail', 'level', 'learning_time', 'students', 'fav_nums', 'cover_image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'level', 'learning_time', 'students', 'fav_nums', 'cover_image', 'click_nums']
    list_filter = list_display


class ChapterAdmin:
    list_display = ['course', 'chapter_name', 'add_time']
    search_fields = ['course', 'chapter_name']
    # course是外键，'course__name'则指明了将外键的name字段作为过滤字段
    list_filter =  ['course__name', 'chapter_name', 'add_time']


class VideoAdmin:
    list_display = ['chapter', 'video_name', 'add_time']
    search_fields = ['chapter', 'video_name']
    list_filter = ['chapter__chapter_name', 'video_name', 'add_time']


class CourseResourceAdmin:
    list_display = ['course', 'resource_name', 'download', 'add_time']
    search_fields = ['course', 'resource_name', 'download']
    list_filter = ['course__name', 'resource_name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
