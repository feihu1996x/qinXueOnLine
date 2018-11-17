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
# from users.views import UnSafeLoginView
from qinXueOnLine import settings

urlpatterns = [
    path((settings.URL_PREFIX + '/admin/').lstrip("/"), xadmin.site.urls),
    path((settings.URL_PREFIX).lstrip("/") + "/", IndexView.as_view(), name='index'),
    # path('login', login, name='login')
    path(settings.LOGIN_URL.lstrip("/"), LoginView.as_view(), name='login'),
    # path('login', UnSafeLoginView.as_view(), name='login'),
    path((settings.URL_PREFIX + '/logout').lstrip("/"), LogoutView.as_view(), name='logout'),
    path((settings.URL_PREFIX + '/register').lstrip("/"), RegisterView.as_view(), name='register'),

    # 验证码url配置
    path((settings.URL_PREFIX + '/captcha').lstrip("/"), include('captcha.urls')),

    # 用户激活url配置
    path((settings.URL_PREFIX + '/active/<str:active_code>').lstrip("/"), ActiveView.as_view()),

    path((settings.URL_PREFIX + '/forgetpwd').lstrip("/"), ForgetPwdView.as_view(), name='forgetpwd'),
    path((settings.URL_PREFIX + '/resetpwd/<str:reset_code>').lstrip("/"), ResetPwdView.as_view(), name='resetpwd'),

    # 课程机构url配置
    url(r'^' + (settings.URL_PREFIX + r'/org/').lstrip("/"), include(('organizations.urls', 'organizations'), namespace="org")),

    # 课程url配置
    url(r'^' + (settings.URL_PREFIX + r'/course/').lstrip("/"), include(('courses.urls', 'courses'), namespace="course")),

    # 用户中心url配置
    url(r'^' + (settings.URL_PREFIX + r'/user/').lstrip("/"), include(('users.urls', 'users'), namespace="user")),

    # 上传文件访问url配置
    url((settings.URL_PREFIX + r'/media/(?P<path>.*)$').lstrip("/"), serve,  {'document_root': settings.MEDIA_ROOT}),

    # 富文本相关url
    url(r'^' + (settings.URL_PREFIX + r'/ueditor/').lstrip("/"), include(('DjangoUeditor.urls', 'ueditor'), namespace="ueditor")),
]

if not settings.DEBUG:  # 生产环境
    urlpatterns.append(url((settings.URL_PREFIX + r'/static/(?P<path>.*)$').lstrip("/"), serve,  {'document_root': settings.STATIC_ROOT}))
    # handler404 = 'users.views.page_not_found'  # 全局404页面配置
    # handler500 = 'users.views.page_error'  # 全局500页面配置
