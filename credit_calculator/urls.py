from django.urls import path
from . import views
from .views import HomeView, signup_func, signin_func, signout_func, MyPage, course_search, new_timetable_item

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', signup_func, name="signup"),
    path('signin/', signin_func, name="signin"),
    path('signout/', signout_func, name="signout"),
    path('mypage/', MyPage.as_view(), name="mypage"),
    path('search/', course_search, name='course_search'),
    path('new_timetable_item/<int:course_id>/<str:semester>/<int:grade>/<str:day_of_week>/<int:period>/<str:classroom>', new_timetable_item, name='new_timetable_item'),
]