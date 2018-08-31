"""
@file: adminx.py
@brief: 
@author: feihu1996.cn
@date: 18-7-10 下午4:21
@version: 1.0
"""

import xadmin

from organizations.models import City, CourseOrg, Teacher


class CityAdmin:
    list_display = ['city_name', 'add_time', 'city_desc']
    search_fields = ['city_name', 'city_desc']
    list_filter = list_display
    model_icon = 'fa fa-car'


class CourseOrgAdmin:
    list_display = ['org_name', 'org_desc', 'click_nums', 'fav_nums', 'cover_image', 'org_address', 'add_time', 'city']
    search_fields = ['org_name', 'org_desc', 'cover_image', 'org_address', 'city']
    list_filter = ['org_name', 'org_desc', 'click_nums', 'fav_nums', 'cover_image', 'org_address', 'add_time', 'city__city_name']
    model_icon = 'fa fa-flag'
    # relfield = 'fk-ajax'  # 设置当某张表的外键指向它的时候，在后台管理系统中不再以默认的下拉框形式出现，而是以ajax异步加载的方式出现,适用于后台条目数量过多的情况


class TeacherAdmin:
    list_display = ['course_org', 'name', 'working_years', 'working_company', 'working_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['course_org__org_name', 'name', 'working_company', 'working_position', 'points']
    list_filter = ['course_org__org_name', 'name', 'working_years', 'working_company', 'working_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    model_icon = 'fa fa-tachometer'


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
