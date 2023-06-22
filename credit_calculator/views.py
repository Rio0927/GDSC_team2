from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from .models import CourseSchedule, Course, Professor, Timetable
from .forms import SignUpForm
from .forms import CourseSearchForm

from django.db.models import Q

#時間割り登録
def timetable(request):
    if request.method == 'POST':
        selected_course_id = request.POST.get('course')  # フォームから選択されたコースのIDを取得
        selected_course = Course.objects.get(pk=selected_course_id)  # IDに基づいてコースオブジェクトを取得
        grade = request.POST.get('grade')  # フォームから成績を取得
        semester = request.POST.get('semester')  # フォームから学期を取得

        # タイムテーブルモデルのインスタンスを作成してデータベースに保存
        timetable = Timetable(course_instance=selected_course, grade=grade, semester=semester)
        timetable.save()

        return redirect('timetable')  # 時間割ページにリダイレクトするなど、適切な処理を行う
    else:
        return render(request, 'form.html')  # フォームを表示するテンプレートを返す


def course_search(request):
    form = CourseSearchForm(request.GET)
    schedules = CourseSchedule.objects.all()

    if form.is_valid():
        semester = form.cleaned_data['semester']
        grade_level = form.cleaned_data['grade_level']
        professor_name = form.cleaned_data['professor_name']

        period_data = {
            CourseSchedule.MONDAY: form.cleaned_data['monday_period'],
            CourseSchedule.TUESDAY: form.cleaned_data['tuesday_period'],
            CourseSchedule.WEDNESDAY: form.cleaned_data['wednesday_period'],
            CourseSchedule.THURSDAY: form.cleaned_data['thursday_period'],
            CourseSchedule.FRIDAY: form.cleaned_data['friday_period'],
            CourseSchedule.SATURDAY: form.cleaned_data['saturday_period'],
        }

        s_objects = Q()
        if semester:
            for s in semester:
                s_objects |= Q(semester=s)
            schedules = schedules.filter(s_objects)
        if grade_level:
            schedules = schedules.filter(course__minimum_grade_level__lte=grade_level)
        if professor_name:
            schedules = schedules.filter(professors__professor__last_name__icontains=professor_name)

        q_objects = Q()
        for day, periods in period_data.items():
            if periods:
                q_objects |= Q(day_of_week=day, period__in=periods)

        schedules = schedules.filter(q_objects)

    return render(request, 'search.html', {'form': form, 'schedules': schedules, 'semester':semester, 'grade_level':grade_level, 'day_and_hour':period_data.items()})


class HomeView(View):
    def get(self, request):
        return render(request, '../templates/home.html', {
            'CourseSchedule': CourseSchedule,
        })

# アカウント作成
def signup_func(request):
    form = SignUpForm
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            #from.cleaned_data.getでフォームの入力値を取得
            lastName = form.cleaned_data.get("last_name")
            firstName = form.cleaned_data.get("first_name")

            #バリデート後にusernameをlast_nameとfirst_nameを結合して作成
            username = lastName + " " +firstName
            eMail = form.cleaned_data.get("email")

            # ユーザーを仮設定、パスワードは下でセットするのでここでは仮のパスワードを設定
            new_user = User(username=username, last_name=lastName, first_name=firstName, email=eMail,password="default_password")

            #パスワードをセット
            new_user.set_password(form.cleaned_data.get("password1"))

            #新しいユーザーを
            new_user.save()

            return redirect("signin")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# サインイン
def signin_func(request):
    if request.method == "POST":

        eMail = request.POST["email"]
        passWord = request.POST["password"]

        print(eMail)
        print(passWord)

        #本来はuser = authenticate()とするのが良いが、email認証だと機能しなかった。
        try:
            user = User.objects.get(email=eMail)
            print("メールアドレスが一致するユーザーを確認しました。")
        except:
            print("メールアドレスが一致するユーザーを確認できませんでした")
            return render (request, "signin.html", {"message":"メールアドレス、またはパズワードが間違っています"})
        
        # メールアドレスが一致するUserを取得した時のみここを通過する

        if check_password(passWord, user.password):
            login(request, user)
            print("ログイン完了！！！")
            return redirect("home")
        else:
            print("パスワードが一致しない")
            return render (request, "signin.html", {"message":"メールアドレス、またはパズワードが間違っています"})
                
    else:
        return render(request, 'signin.html')

#　サインアウト
def signout_func(request):
    logout(request)
    return redirect('home')

class MyPage(TemplateView):
    template_name = "mypage.html"