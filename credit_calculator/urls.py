from django.urls import path
from . import views
from .views import HomeView, CourseView

urlpatterns = [
    path('courses/<str:day_of_week>/', CourseView.as_view(), name='courses'),
    path('', HomeView.as_view(), name='home'),
]