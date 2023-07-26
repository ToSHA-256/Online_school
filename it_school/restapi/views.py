from rest_framework import generics, status, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from rest_framework.response import Response
from django.http import Http404
from mainpage.models import Course, Lesson
from registration.models import CustomUser
from .serializers import CourseSerializer, CustomUserSerializer, LessonSerializer, LessonDetailSerializer
from .permissions import IsCourseOwner


class CourseListViewAPI(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save()


class CourseDetailViewAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'


class PersonalCabinetView(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = CustomUserSerializer(user)
        username = user.username
        data = serializer.data
        data["greeting"] = f"Hello, {username}"
        return Response(data, status=status.HTTP_200_OK)


class CourseLessonsListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        course_id = self.kwargs['course_id']

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Lesson.objects.none()

        is_course_added = user.courses.filter(id=course_id).exists()

        if not is_course_added:
            return Lesson.objects.none()

        lessons = Lesson.objects.filter(course_owner=course)
        return lessons


class LessonDetailViewAPI(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseOwner]

    def get_object(self):
        lesson_id = self.kwargs['lesson_id']
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            return lesson
        except Lesson.DoesNotExist:
            raise Http404("Lesson does not exist")

