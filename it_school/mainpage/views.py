from tabulate import tabulate
from .models import Course, Lesson, CustomGroup, CustomUser, Attendance, ChatMessage, TECHNOLOGIES
from django.views.generic import DetailView, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, redirect
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from django.http import HttpResponse
import json

from django.shortcuts import render
from .models import Lesson
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@csrf_protect
def index(request):
    course_object = Course.objects.all()
    for i in course_object:
        i.img = str(i.img)[5:]
        i.imgTech = str(i.tech_img)[5:]
    data = {
        'title': 'Online school',
        'page_label': 'Главная страница',
        'courses': course_object,
        'technology': ['Все технологии'] + TECHNOLOGIES,
        'difficulty': ['Любая сложность', 'Начинающий', 'Продвинутый'],
    }
    template = 'mainpage.html'
    return render(request, template, data)


def lesson_list(request):
    lessons = Lesson.objects.all()
    context = {'lessons': lessons}
    return render(request, 'lesson_list.html', context)


def course_lessons(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course_owner=course)
    return render(request, 'course_lissons.html', {'course': course, 'lessons': lessons})




def personal_cabinet(request):
    user = request.user
    courses = user.courses.all().order_by('start_date')  # Получаем список курсов пользователя, отсортированных по дате начала

    # Создаем пустой словарь для хранения уроков по курсам
    lessons_by_course = {}

    # Получаем список уроков для каждого курса
    for course in courses:
        lessons = Lesson.objects.filter(course_owner=course)
        lessons_by_course[course] = lessons

    return render(request, 'personal_cabinet.html', {'user': user, 'courses': courses, 'lessons_by_course': lessons_by_course})


class CourseDetailView(DetailView):
    error = ''
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

    def post(self, request, *args, **kwargs):
        if 'confirm_payment' in request.POST:
            course = self.get_object()
            user = request.user
            course_price = course.price

            if user.wallet >= course_price:
                user.wallet -= course_price
                user.save()
                messages.success(request, 'Оплата прошла успешно.')
                return redirect('purchase_confirmation', pk=course.pk)
            else:
                self.error = 'Недостаточно средств на счете.'

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = self.error
        if self.error:
            context['styleconfp'] = 'display: flex;'
        return context


def purchase_confirmation(request, pk):
    course = Course.objects.get(id=pk)
    return render(request, 'purchase_confirmation.html', {'course': course})


def attendance_table(request):
    groups = CustomGroup.objects.all()
    attendance_tables = []

    for group in groups:
        lessons = Lesson.objects.filter(course_owner=group.course_owner)
        students = CustomUser.objects.filter(groups=group)
        attendance = Attendance.objects.filter(group=group)

        print(f'{students}')

        table = []
        table_headers = ['Слушатель'] + [str(lesson.start_date) for lesson in lessons]

        for student in students:
            row = [student.get_full_name()]
            for lesson in lessons:
                attendance_entry = attendance.get(lesson=lesson, student=student)
                row.append(attendance_entry.attended)
            table.append(row)

        attendance_tables.append({
            'group': group,
            'table': tabulate(table, headers=table_headers, tablefmt='grid')
        })

    return render(request, 'attendance.html', {'attendance_tables': attendance_tables})



def chat_room(request, group_id):
    group = get_object_or_404(CustomGroup, id=group_id)
    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_add)(f'chat_group_{group_id}', 'websocket_group')

    return render(request, 'room.html', {'group': group, 'messages': messages})



def send_message(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(CustomGroup, id=group_id)
        sender = request.user
        message_text = request.POST.get('message_text')
        if message_text:
            ChatMessage.objects.create(sender=sender, group=group, text=message_text)
    return redirect('chat_room', group_id=group_id)