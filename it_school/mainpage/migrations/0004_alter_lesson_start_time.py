# Generated by Django 4.2.2 on 2023-07-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_lesson_is_past_alter_lesson_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='start_time',
            field=models.TimeField(default='19:00', verbose_name='Время начала курса'),
        ),
    ]