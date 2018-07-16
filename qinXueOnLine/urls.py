"""qinXueOnLine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
# from django.views.generic import TemplateView
from django.views.static import serve
from django.conf.urls import url

import xadmin

# from users.views import login
from users.views import LoginView, LogoutView ,RegisterView, ActiveView, ForgetPwdView, ResetPwdView, IndexView
from qinXueOnLine import settings

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    # path('login', login, name='login')
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('captcha', include('captcha.urls')),
    path('active/<str:active_code>', ActiveView.as_view()),
    path('forgetpwd', ForgetPwdView.as_view(), name='forgetpwd'),
    path('resetpwd/<str:reset_code>', ResetPwdView.as_view(), name='resetpwd'),

    # 课程机构url配置
    url(r'^org/', include(('organizations.urls', 'organizations'), namespace="org")),

    # 课程url配置
    url(r'^course/', include(('courses.urls', 'courses'), namespace="course")),

    # 用户中心url配置
    url(r'^user/', include(('users.urls', 'users'), namespace="user")),

    # 上传文件访问url配置
    url(r'media/(?P<path>.*)$', serve,  {'document_root': settings.MEDIA_ROOT})
]

if not settings.DEBUG:  # 生产环境
    urlpatterns.append(url(r'static/(?P<path>.*)$', serve,  {'document_root': settings.STATIC_ROOT}))
    # handler404 = 'users.views.page_not_found'  # 全局404页面配置
    # handler500 = 'users.views.page_error'  # 全局500页面配置
