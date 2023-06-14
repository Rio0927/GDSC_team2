from django.urls import path
from . import views
from .views import HomeView, CourseView, signup_func, signin_func, signout_func, MyPage

urlpatterns = [
    path('courses/<str:day_of_week>/', CourseView.as_view(), name='courses'),
    path('', HomeView.as_view(), name='home'),
    path('signup/', signup_func, name="signup"),
    path('signin/', signin_func, name="signin"),
    path('signout/', signout_func, name="signout"),
    path('mypage/', MyPage.as_view(), name="mypage"),
]