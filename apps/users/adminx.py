"""
@file: adminx.py
@brief: adminx
@author: feihu1996.cn
@date: 18-7-10 下午3:02
@version: 1.0
"""

import xadmin
from xadmin import views

from users.models import EmailVerifyRecord
from users.models import Banner


class BaseSetting:
    """
    xadmin全局配置类
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    """
    xadmin全局配置类
    """
    site_title = '勤学在线后台管理系统'
    site_footer = '勤学在线网'
    # 折叠左侧菜单
    menu_style = 'accordion'


class EmailVerifyRecordAdmin:
    # 自定义列表页显示字段
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 自定义检索字段
    search_fields = ['code', 'email', 'send_type']
    # 自定义筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin:
    # 自定义列表页显示字段
    list_display = ['title', 'cover_image', 'target_url', 'index', 'add_time']
    # 自定义检索字段
    search_fields = ['title', 'cover_image', 'target_url', 'index']
    # 自定义筛选字段
    list_filter = ['title', 'cover_image', 'target_url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
