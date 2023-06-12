from django.views import View
from django.shortcuts import render
from .models import CourseSchedule

class CourseView(View):
    def get(self, request, day_of_week=None):
        courses = CourseSchedule.objects.filter(day_of_week=day_of_week).select_related('course_instance__course')

        return render(request, 'credit_calculator/courses.html', {
            'day_of_week': day_of_week,
            'courses': courses,
        })

class HomeView(View):
    def get(self, request):
        return render(request, 'credit_calculator/home.html', {
            'CourseSchedule': CourseSchedule,
        })


