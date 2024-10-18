from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']  # Adjust fields as necessary


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


from django.conf import settings  # Make sure to import settings if not done already


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        send_mail(
            subject='Регистрация на Новостном портале',
            message=f'Здравствуйте, {user.username}! Добро пожаловать на Новостной портал!',
            from_email=settings.DEFAULT_FROM_EMAIL,  # Corrected typo here
            recipient_list=[user.email],
        )

        return user
