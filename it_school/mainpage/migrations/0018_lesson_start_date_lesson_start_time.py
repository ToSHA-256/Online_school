# Generated by Django 4.2.2 on 2023-06-16 08:54

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0017_lesson_mentor_owner_alter_lesson_course_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='lesson',
            name='start_time',
            field=models.TimeField(default=datetime.time(19, 0)),
        ),
    ]