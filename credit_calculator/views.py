from django.views import View
from django.shortcuts import render, redirect
from .models import CourseSchedule
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout

class CourseView(View):
    def get(self, request, day_of_week=None):
        courses = CourseSchedule.objects.filter(day_of_week=day_of_week)#.select_related('course_schedule__course')

        return render(request, '../templates//courses.html', {
            'day_of_week': day_of_week,
            'courses': courses,
        })

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