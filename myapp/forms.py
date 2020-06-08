from django import forms
from .models import *
# ログイン・サインアップ
from django.forms import EmailField

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# お問い合わせ
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

class PostForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ('title', 'url', 'address', 'corner_title','genrelist',)

    # チェックボックスに切替
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            self.fields['genrelist'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'control'}) 
            self.fields['genrelist'].queryset = Genre.objects

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class StationForm(forms.ModelForm):

    class Meta:
        model = Station
        fields = '__all__'

    # チェックボックスに切替
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            self.fields['day_of_the_week'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'control'}) 
            self.fields['day_of_the_week'].queryset = Week.objects



class WeekForm(forms.ModelForm):

    class Meta:
        model = Week
        fields = ('weeks',)


class DjForm(forms.ModelForm):

    class Meta:
        model = Dj
        fields = ('dj_name', 'main_dj',)

class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = ('genre_name',)

class ListenerForm(forms.ModelForm):

    class Meta:
        model = Listener
        fields = ('listener_name',)

class OkiniForm(forms.ModelForm):

    class Meta:
        model = Okini
        fields = ('user','program')

StationFormset = forms.inlineformset_factory(
    # 親親モデル
    parent_model = Program,
    # 子モデル
    model = Station,
    form = StationForm,
    fields='__all__',
    extra=1, can_delete=False
)

DjFormset = forms.inlineformset_factory(
    Program, Dj,  fields='__all__',
    extra=5, can_delete=False
)

ListenerFormset = forms.inlineformset_factory(
    Program, Listener,  fields='__all__',
    extra=3, can_delete=False
)

# ログイン・サインアップ
# class SignUpForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password1', 'password2')

#     def save(self, commit=True):
#         user = super(SignUpForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user


User = get_user_model()


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email','username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email','username','profile')

# お問い合わせ
class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "お問い合わせ"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]  # 受信者リスト
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

# 意見箱
class OpinionForm(forms.ModelForm):

    class Meta:
        model = Opinion
        fields = ('name','text')