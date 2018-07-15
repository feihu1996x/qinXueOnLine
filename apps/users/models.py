from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    """
    通过UserProfile覆盖默认User表
    """
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), default='female', max_length=6, verbose_name='性别')
    address = models.CharField(max_length=100, default='', verbose_name='住址')
    cell_phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    head_shot = models.ImageField(upload_to='resource/images/head_shot/%Y/%m', default='resource/images/head_shot/default.png', max_length=100, verbose_name='用户头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_unread_message_nums(self):
        """
        获取用户未读消息的数量
        :return:
        """
        from userOperations.models import UserMessage
        from django.db.models import Q
        return UserMessage.objects.filter(Q(user=self.id)|Q(user=0),Q(has_read=False)).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=10, choices=(('register', '注册'), ('forget', '找回密码'), ('update', '更新邮箱')), verbose_name='验证类型')
    send_time = models.DateField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}({})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    cover_image = models.ImageField(upload_to='resource/images/banner_cover/%Y/%m', verbose_name='轮播图', max_length=100)
    target_url = models.URLField(max_length=100, verbose_name='链接地址')
    index = models.IntegerField(default=100, verbose_name='轮播顺序')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
