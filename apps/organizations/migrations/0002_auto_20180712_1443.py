# Generated by Django 2.0.7 on 2018-07-12 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city_desc',
            field=models.TextField(verbose_name='城市描述'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='cover_image',
            field=models.ImageField(upload_to='resource/images/org_cover/%Y/%m', verbose_name='封面图'),
        ),
    ]
