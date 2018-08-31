import json

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auto_login
from django.contrib.auth import logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UserImageUploadModelForm, UserModifyPwdForm, UserInfoModelForm
from users.models import UserProfile, EmailVerifyRecord, Banner
from userOperations.models import UserCourse, UserFavorite, UserMessage
from utils.send_email import send_email
from utils.mixin_utils import LoginRequiredMixin
from organizations.models import CourseOrg
from organizations.models import Teacher
from courses.models import Course


class CustomBackend(ModelBackend):
    """
    重载authenticate用户认证函数
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 根据username查询user
            # 这里传进来的username参数既可以是用户名也可以是邮箱地址
            # 通过Q类，实现字段的或查询
            # 进而实现了通过用户名和邮箱都能登录
            user_model = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 校验密码
            if user_model.check_password(password):
                return user_model
        except:
            return None


# Create your views here.
# def login(request):
#     """
#     :用户登录请求处理函数(建议用类来处理用户请求)
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user_model = authenticate(username=username, password=password)
#         if user_model is not None:
#             # 用户登录认证通过
#             auto_login(request, user_model)
#             return render(request, 'index.html')
#         else:
#             # 用户登录认证未通过
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})


# class UnSafeLoginView(View):
#     """
#     不安全的登录机制演示（SQL注入）
#     """
#     def get(self, request):
#         return render(request, 'login.html', {})
#
#     def post(self, request):
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#
#         import MySQLdb
#         conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='9f%IFhJ618', db='qinXueOnLine', charset='utf8')
#         cursor = conn.cursor()
#         # 当不法分子提交过来的表单中的username值为"' OR 1=1#"时就会跳过用户认证，即构成了SQL注入，
#         select_sql = "select * from users_userprofile where username='{0}' and password='{1}'".format(username, password)
#         result = cursor.execute(select_sql)
#         if result:
#             print("查询到用户")
#         else:
#             print("没有查询到用户")
#         return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    """
    用户登录请求处理类
    """
    def get(self, request):
        """
        :如果是get请求
        :param request:
        :return:
        """
        all_banner_course_records = Course.objects.filter(is_banner=True)[:3]
        return render(request, 'login.html', {
            'all_banner_course_records': all_banner_course_records
        })

    def post(self, request):
        """
        ；如果是post请求
        :param request:
        :return:
        """
        login_form = LoginForm(request.POST)
        all_banner_course_records = Course.objects.filter(is_banner=True)[:3]
        if login_form.is_valid():  # 用户登录提交表单字段验证成功
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user_model = authenticate(username=username, password=password)
            if user_model is not None:  # 用户登录认证通过
                if user_model.is_active:  # 用户已经激活
                    auto_login(request, user_model)
                    # TODO：向用户发送一条消息，“尊敬的xxx用户, 欢迎回来”
                    user_message_model = UserMessage()
                    user_message_model.user = user_model.id
                    user_message_model.message_content = '欢迎来到勤学网～'
                    user_message_model.save()
                    return HttpResponseRedirect(reverse('index'))
                else:  # 用户未激活
                    return render(request, 'login.html', {'msg': '用户尚未激活！', 'login_form': login_form, 'all_banner_course_records': all_banner_course_records})
            else:  # 用户登录认证未通过
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form, 'all_banner_course_records': all_banner_course_records})
        else:
            # 用户登录提交表单字段验证失败
            return render(request, 'login.html', {'login_form': login_form, 'all_banner_course_records': all_banner_course_records})


class LogoutView(View):
    """
    用户退出登录请求处理类
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))  # 重定向到index页面, reverse函数用于将url名称反向解析成真实的url


class RegisterView(View):
    """
    用户注册请求处理类
    """
    def get(self, request):
        register_form = RegisterForm()
        all_banner_course_records = Course.objects.filter(is_banner=True)[:3]
        return render(request, 'register.html', {
            'register_form': register_form,
            'all_banner_course_records': all_banner_course_records
        })

    def post(self, request):
        register_form = RegisterForm(request.POST)
        all_banner_course_records = Course.objects.filter(is_banner=True)[:3]

        if register_form.is_valid():  # 用户注册提交表单字段验证成功
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')

            try:
                UserProfile.objects.get(Q(username=email)|Q(email=email))  # 查询当前注册用户是否已经存在
            except:  # 将用户注册信息写入数据库
                user_model = UserProfile()
                user_model.username = email
                user_model.email = email
                user_model.password = make_password(password=password)
                user_model.is_active = False # 用户尚未激活
                user_model.save()
                send_email(email)  # 发送注册激活链接
                return render(request, 'login.html', {'msg': '注册激活链接已经发送到您的邮箱'})
            else:
                return render(request, 'register.html', {
                    'msg': '用户已经存在！',
                    'register_form': register_form,
                    'all_banner_course_records': all_banner_course_records
                })

        else:  # 用户注册提交表单字段验证失败
            return render(request, 'register.html', {
                'register_form': register_form,
                'all_banner_course_records': all_banner_course_records
            })


class ActiveView(View):
    """
    用户激活请求处理类
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

            return render(request, 'login.html', {'msg': '用户已经激活，请登录！'})
        else:
            return render(request, 'active_fail.html', {'msg': '激活链接失效！'})


class ForgetPwdView(View):
    """
    找回密码请求处理类
    """
    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        all_banner_course_records = Course.objects.filter(is_banner=True)[:3]
        return render(request, 'forgetpwd.html', {
            'forget_pwd_form': forget_pwd_form,
            'all_banner_course_records': all_banner_course_records
        })

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        all_banner_course_records = Course.objects.filter(is_banner=True)[:3]
        if forget_pwd_form.is_valid():  # 找回密码表单字段验证成功
            email = request.POST.get('email', '')
            send_email(email=email, send_type='forget')  # 发送找回密码链接
            return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form, 'msg': '重置密码链接已经发送到您的邮箱！', 'all_banner_course_records': all_banner_course_records})
        else:
            return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form, 'all_banner_course_records': all_banner_course_records})


class ResetPwdView(View):
    """
    重置密码请求处理类
    """
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'password_reset.html', {'msg': '链接失效！'})

    def post(self, request, reset_code):
        all_banner_course_records = Course.objects.filter(is_banner=True)[:3]
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            password = request.POST.get('password', '')
            re_password = request.POST.get('password1', '')
            email = request.POST.get('email', '')

            if password != re_password:  # 两次密码输入不一致
                return render(request, 'password_reset.html', {'email': email, 'reset_pwd_form': reset_pwd_form, 'msg': '两次密码不一致，请重新输入'})
            else: # 保存新密码
                user_model = UserProfile.objects.get(email=email)
                user_model.password = make_password(password=password)
                user_model.save()
                return render(request, 'login.html', {'msg': '密码重置成功，请重新登录', 'all_banner_course_records': all_banner_course_records})
        else:
            return render(request, 'password_reset.html', {'email': reset_pwd_form.data.get('email'), 'reset_pwd_form': reset_pwd_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户资料请求处理类
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_model_form = UserInfoModelForm(request.POST, instance=request.user)
        if user_info_model_form.is_valid():
            user_info_model_form.save()
            return HttpResponse('{"status":0, "msg": "资料保存成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_model_form.errors), content_type='application/json')


class UserImageUploadView(LoginRequiredMixin, View):
    """
    用户上传头像请求处理类
    """
    def post(self, request):
        user_image_upload_model_form = UserImageUploadModelForm(request.POST, request.FILES, instance=request.user)
        if user_image_upload_model_form.is_valid():
            """
            head_shot = user_image_upload_model_form.cleaned_data['head_shot']  # user_image_upload_model_form.cleaned_data保存的是已经验证通过的字段
            request.user.head_shot = head_shot
            request.user.save()
            """
            user_image_upload_model_form.save(commit=True)
            return HttpResponse('{"status":0}', content_type='application/json')
        else:
            return HttpResponse('{"status":1, "msg": "头像上传失败"}', content_type='application/json')


class UserModifyPwdView(LoginRequiredMixin, View):
    """
    用户修改密码请求处理类
    """

    def post(self, request):
        modify_pwd_form = UserModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            password = request.POST.get('password', '')
            re_password = request.POST.get('password1', '')

            if password != re_password:  # 两次密码输入不一致
                return HttpResponse('{"status":1, "msg": "两次密码输入不一致"}', content_type='application/json')
            else:  # 保存新密码
                user_model = request.user
                user_model.password = make_password(password=password)
                user_model.save()
                return HttpResponse('{"status":0, "msg": "密码修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码请求处理类
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):  # 邮箱已经被占用
            return HttpResponse('{"status":1, "msg": "邮箱已经被占用"}', content_type='application/json')

        send_email(email=email, send_type='update')
        return HttpResponse('{"status":0, "msg": "邮箱验证码发送成功"}', content_type='application/json')


class UserModifyEmailView(LoginRequiredMixin ,View):
    """
    用户修改邮箱请求处理类
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update'):  # 如果邮箱验证码匹配正确
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":0, "msg": "邮箱修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":1, "msg": "邮箱修改失败"}', content_type='application/json')


class UserMyCourseView(LoginRequiredMixin ,View):
    """
    用户课程请求处理类
    """
    def get(self, request):
        user_course_records = UserCourse.objects.filter(user=request.user)

        return render(request, 'usercenter-mycourse.html', {
            'user_course_records': user_course_records
        })


class UserFavOrgView(LoginRequiredMixin, View):
    """
    用户收藏机构请求处理类
    """
    def get(self, request):
        all_user_fav_records =  UserFavorite.objects.filter(user=request.user, fav_type=2)
        all_user_fav_org_ids = [user_fav_record.fav_id for user_fav_record in all_user_fav_records]
        all_user_fav_org_records = CourseOrg.objects.filter(id__in=all_user_fav_org_ids)
        return render(request, 'usercenter-fav-org.html', {
            'all_user_fav_org_records': all_user_fav_org_records
        })


class UserFavTeacherView(LoginRequiredMixin,View):
    """
    用户收藏教师请求处理类
    """
    def get(self, request):
        all_user_fav_records = UserFavorite.objects.filter(user=request.user, fav_type=3)
        all_user_fav_teacher_ids = [user_fav_record.fav_id for user_fav_record in all_user_fav_records]
        all_user_fav_teacher_records = Teacher.objects.filter(id__in=all_user_fav_teacher_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'all_user_fav_teacher_records': all_user_fav_teacher_records
        })


class UserFavCourseView(LoginRequiredMixin, View):
    """
    用户收藏课程请求处理类
    """
    def get(self, request):
        all_user_fav_records = UserFavorite.objects.filter(user=request.user, fav_type=1)
        all_user_fav_course_ids = [user_fav_record.fav_id for user_fav_record in all_user_fav_records]
        all_user_fav_course_records = Course.objects.filter(id__in=all_user_fav_course_ids)
        return render(request, 'usercenter-fav-course.html', {
            'all_user_fav_course_records': all_user_fav_course_records
        })


class UserMessageView(LoginRequiredMixin, View):
    """
    用户消息请求处理类
    """
    def get(self, request):
        all_user_messages =  UserMessage.objects.filter(Q(user=0)|Q(user=request.user.id))

        # 将所有未读消息变为已读
        all_unread_user_messages = UserMessage.objects.filter(Q(user=request.user.id)|Q(user=0), has_read=False)
        for unread_user_message in all_unread_user_messages:
            unread_user_message.has_read = True
            unread_user_message.save()

        # 对用户消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_user_messages, 5, request=request)
        all_user_messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'all_user_messages': all_user_messages
        })


class IndexView(View):
    """
    勤学在线网首页请求处理类
    """
    def get(self, request):
        all_bannner_records = Banner.objects.all().order_by('index')  # 首页大轮播图
        all_not_banner_course_records = Course.objects.filter(is_banner=False)[:6]  # 非轮播图课程
        all_banner_course_records = Course.objects.filter(is_banner=True)[:3]  # 轮播图课程（首页中间）
        all_course_org_records = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_bannner_records': all_bannner_records,
            'all_not_banner_course_records': all_not_banner_course_records,
            'all_banner_course_records': all_banner_course_records,
            'all_course_org_records': all_course_org_records
        })

# 404,403,500等错误请求处理函数
# Django 2.0版本貌似已经不需要再自定义处理函数,只需要准备好相应的页面即可

# def page_not_found(request):
#     """
#     404错误请求处理函数
#     :param request:
#     :return:
#     """
#     from django.shortcuts import render_to_response
#     response = render_to_response('404.html', {})
#     response.status_code = 404
#     return response


# def page_error(request):
#     # 500错误请求处理函数
#     from django.shortcuts import render_to_response
#     response = render_to_response('500.html', {})
#     response.status_code = 500
#     return response
