# Generated by Django 2.0.7 on 2018-07-10 02:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=20, verbose_name='城市名称')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('city_desc', models.CharField(max_length=200, verbose_name='城市描述')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=50, verbose_name='机构名称')),
                ('org_desc', models.TextField(verbose_name='机构描述')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('cover_image', models.ImageField(upload_to='images/org_cover/%Y/%m', verbose_name='封面图')),
                ('org_address', models.CharField(max_length=150, verbose_name='机构地址')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.City', verbose_name='所在城市')),
            ],
            options={
                'verbose_name': '课程机构',
                'verbose_name_plural': '课程机构',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('working_years', models.IntegerField(default=0, verbose_name='工作年限')),
                ('working_company', models.CharField(max_length=50, verbose_name='就职公司')),
                ('working_position', models.CharField(max_length=50, verbose_name='公司职位')),
                ('points', models.CharField(max_length=50, verbose_name='教学特点')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.CourseOrg', verbose_name='所属机构')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
        ),
    ]
