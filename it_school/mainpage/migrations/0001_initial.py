# Generated by Django 4.2.2 on 2023-07-11 11:19

import datetime
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mainpage.fields
import mainpage.models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_mentor', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, verbose_name='Полное описание')),
                ('short_des', models.TextField(default='', max_length=100, verbose_name='Краткое описание')),
                ('difficulty', models.CharField(choices=[('Начинающий', 'Beginner'), ('Продвинутый', 'Advanced')], max_length=15, verbose_name='Сложность курса')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='Рейтинг курса')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Стоимость курса')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата начала курса')),
                ('start_time', models.TimeField(default=datetime.time(19, 0), verbose_name='Время начала курса')),
                ('days_of_week', multiselectfield.db.fields.MultiSelectField(choices=[('monday', 'понедельник'), ('tuesday', 'вторник'), ('wednesday', 'среда'), ('thursday', 'четверг'), ('friday', 'пятница'), ('saturday', 'суббота'), ('sunday', 'воскресенье')], default='monday', max_length=56, validators=[django.core.validators.MaxValueValidator(7)], verbose_name='Дни недели занятий')),
                ('technologies', multiselectfield.db.fields.MultiSelectField(choices=[('Python', 'Python'), ('C++', 'C++'), ('Java', 'Java'), ('C#', 'C#'), ('Pascal', 'Pascal'), ('Frontend', 'Frontend')], default='Python', max_length=34, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Применяемы языки')),
                ('lessons_count', models.IntegerField(default=1)),
                ('img', mainpage.fields.WEBPField(default='mainpage/static/dist/img/Models/no_image_big.png', upload_to=mainpage.models.image_folder_Course, verbose_name='Изображение курса')),
                ('tech_img', mainpage.fields.WEBPField(default='mainpage/static/dist/img/Models/no_image_big.png', upload_to=mainpage.models.image_folder_Technology, verbose_name='Изображение языка')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='CustomGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Lesson 1', max_length=255)),
                ('material', models.TextField(default='Полное описание', verbose_name='Полное описание')),
                ('day_of_week', models.CharField(choices=[('monday', 'понедельник'), ('tuesday', 'вторник'), ('wednesday', 'среда'), ('thursday', 'четверг'), ('friday', 'пятница'), ('saturday', 'суббота'), ('sunday', 'воскресенье')], default='monday', max_length=10)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('start_time', models.TimeField(default='19:00', verbose_name='Время начала курса')),
                ('is_past', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objective', to='mainpage.course')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]
