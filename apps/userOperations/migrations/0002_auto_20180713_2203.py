# Generated by Django 2.0.7 on 2018-07-13 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userOperations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecomments',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
    ]
