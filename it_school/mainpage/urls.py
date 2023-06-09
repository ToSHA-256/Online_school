from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import include, path
import registration.views

from .views import CourseDetailView, purchase_confirmation, index, attendance_table, personal_cabinet, course_lessons, \
    about_us_view

from registration.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('', index, name='index'),
    # В случае кэшировании класса -> path('', cache_page(60)(UnitsView.as_view()), name='index'),
    path('api/', include('restapi.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('personal_cabinet/', personal_cabinet, name='personal_cabinet'),
    path('about/', about_us_view, name='about_us'),
    path('course/<int:course_id>/lessons/', course_lessons, name='course_lessons'),
    path('<int:pk>', CourseDetailView.as_view(), name='course_detail'),
    path('attendance/', attendance_table, name='attendance_table'),
    path('purchase_confirmation/<int:pk>/', purchase_confirmation, name='purchase_confirmation'),

]
