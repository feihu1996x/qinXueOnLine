from datetime import datetime


from django.db import models


# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=20, verbose_name='城市名称')
    add_time = models.DateField(default=datetime.now,verbose_name='添加时间')
    city_desc = models.TextField(verbose_name='城市描述')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city_name


class CourseOrg(models.Model):
    student_nums = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    category = models.CharField(verbose_name='机构类别', max_length=20, choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')), default='pxjg')
    org_name = models.CharField(max_length=50, verbose_name='机构名称')
    org_desc = models.TextField(verbose_name='机构描述')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    cover_image = models.ImageField(upload_to='resource/images/org_cover/%Y/%m', verbose_name='封面图')
    org_address = models.CharField(max_length=150, verbose_name='机构地址')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')
    city = models.ForeignKey(City, verbose_name='所在城市', on_delete=models.CASCADE)
    tag = models.CharField(default='万事皆空', verbose_name='机构标签', max_length=50)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.org_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()


class Teacher(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='所属机构', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='姓名')
    working_years = models.IntegerField(default=0, verbose_name='工作年限')
    working_company = models.CharField(max_length=50, verbose_name='就职公司')
    working_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')
    head_shot = models.ImageField(upload_to='resource/images/head_shot/%Y/%m', default='resource/images/head_shot/default.png' ,max_length=100, verbose_name='讲师头像')
    age = models.IntegerField(default=20, verbose_name='年龄')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()
