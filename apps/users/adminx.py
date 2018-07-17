"""
@file: adminx.py
@brief: adminx
@author: feihu1996.cn
@date: 18-7-10 下午3:02
@version: 1.0
"""

# from django.contrib.auth.models import User

import xadmin
from xadmin import views
# from xadmin.plugins.auth import UserAdmin

from users.models import EmailVerifyRecord
from users.models import Banner
# from users.models import UserProfile


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
    model_icon = 'fa fa-envelope'


class BannerAdmin:
    # 自定义列表页显示字段
    list_display = ['title', 'cover_image', 'target_url', 'index', 'add_time']
    # 自定义检索字段
    search_fields = ['title', 'cover_image', 'target_url', 'index']
    # 自定义筛选字段
    list_filter = ['title', 'cover_image', 'target_url', 'index', 'add_time']
    model_icon = 'fa fa-file-powerpoint-o'


# class UserProfileAdmin(UserAdmin):
#     def get_form_layout(self):
#         if self.org_obj:
#             self.form_layout = (
# 	            Main(
# 	                Fieldset('',
# 	                         'username', 'password',
# 	                         css_class='unsort no_title'
# 	                    ),
# 	                Fieldset(_('Personal info'),
# 	                         Row('first_name', 'last_name'),
# 	                         'email'
# 	                    ),
# 	                Fieldset(_('Permissions'),
# 	                         'groups', 'user_permissions'
# 	                    ),
# 	                Fieldset(_('Important dates'),
# 	                         'last_login', 'date_joined'
# 	                    ),
# 	            ),
# 	            Side(
# 	                Fieldset(_('Status'),
# 	                    'is_active', 'is_staff', 'is_superuser',
# 	                ),
# 	            )
# 	        )
#         return super(UserAdmin, self).get_form_layout()


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)


# xadmin.site.unregister(User)
# xadmin.site.register(UserProfile, UserProfileAdmin)
