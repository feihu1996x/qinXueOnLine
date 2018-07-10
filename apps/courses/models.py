from datetime import datetime

from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.CharField(verbose_name='课程详情', max_length=500)
    level = models.CharField(choices=(('primary', '初级'), ('intermediate', '中级'), ('senior', '高级')), max_length=20, verbose_name='难度')
    learning_time = models.IntegerField(default=0, verbose_name='学习时长（分钟）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    cover_image = models.ImageField(upload_to='resource/images/course_cover/%Y/%m', verbose_name='课程封面', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=100, verbose_name='章节名称')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.chapter_name


class Video(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name='章节', on_delete=models.CASCADE)
    video_name = models.CharField(max_length=100, verbose_name='视频名称')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频基本信息'
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
