# Generated by Django 2.0.7 on 2018-07-12 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20180712_1846'),
        ('courses', '0002_auto_20180710_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.CourseOrg', verbose_name='课程机构'),
        ),
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('primary', '初级'), ('intermediate', '中级'), ('senior', '高级')], max_length=20, verbose_name='难度'),
        ),
    ]
