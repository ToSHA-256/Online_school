from django.urls import path
from .views import CourseListViewAPI, CourseDetailViewAPI
from .views import ChatMessageListCreateViewAPI

from django.urls import include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'courses', CourseListViewAPI, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/', CourseDetailViewAPI.as_view(), name='info-courses'),
    path('chat/', ChatMessageListCreateViewAPI.as_view(), name='chat-messages'),
]
