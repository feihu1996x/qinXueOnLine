from datetime import datetime

from django.db import models
from organizations.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


# Create your models here.
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.TextField(verbose_name='课程描述')
    # detail = models.TextField(verbose_name='课程详情', max_length=500)
    detail = UEditorField(verbose_name='课程详情',
                          width=600,
                          height=300,
                          imagePath='resource/ueditor/',
                          filePath='resource/ueditor/',
                          default='')  # 将detail字段展示成富文本
    level = models.CharField(choices=(('primary', '初级'), ('intermediate', '中级'), ('senior', '高级')), max_length=20, verbose_name='难度')
    learning_time = models.IntegerField(default=0, verbose_name='学习时长（分钟）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    cover_image = models.ImageField(upload_to='resource/images/course_cover/%Y/%m', verbose_name='课程封面', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')
    course_category = models.CharField(verbose_name='课程类别', max_length=30, default='刺客组织')
    course_tag = models.CharField(default='', max_length=50, verbose_name='课程标签')
    teacher = models.ForeignKey(Teacher, verbose_name='课程讲师', null=True, blank=True, on_delete=models.CASCADE)
    essential_skill = models.CharField(max_length=300,  verbose_name='课程须知', default='')
    course_target = models.CharField(max_length=300, verbose_name='课程目标', default='')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_chapter_nums(self):
        """
        课程章节数
        :return:
        """
        return self.chapter_set.all().count()
    get_chapter_nums.short_description = '章节数'

    def get_course_users(self):
        """
        获取课程学习用户
        :return:
        """
        return self.usercourse_set.all()

    def get_course_chapters(self):
        """
        获取课程章节
        :return:
        """
        return self.chapter_set.all()

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.feihu1996.cn">跳转</a>')
    go_to.short_description = '跳转'


class BannerCourse(Course):
    """
    对轮播图课程和非轮播图课程分开管理，
    在xadmin中对应不同的管理器，
    但在数据库中其实是同一张表
    """
    class Meta:
        verbose_name = '轮播图课程'
        verbose_name_plural = verbose_name
        proxy = True  # 只有当proxy值为True时，此model才不会单独在数据库中再生成一张表


class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=100, verbose_name='章节名称')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.chapter_name

    def get_chapter_videos(self):
        return self.video_set.all()


class Video(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name='章节', on_delete=models.CASCADE)
    video_name = models.CharField(max_length=100, verbose_name='视频名称')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')
    video_source = models.URLField(verbose_name='资源地址', max_length=300, default='')
    video_times = models.IntegerField(default=0, verbose_name='视频时长')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.video_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=100, verbose_name='资源名称')
    download = models.FileField(upload_to='resource/course/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.resource_name
