#templateでのフォームを作りやすくしてくれるファイル

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=True, #必須項目
        # help_text="必須",
        label="First Name",
    )

    last_name = forms.CharField(
        max_length=50,
        required=True, #必須項目
        # help_text="必須",
        label="Last Name",
    )

    email = forms.EmailField(
        max_length=254,
        label='Email Adress'
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")
