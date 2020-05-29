from django import forms
from .models import *
# ログイン・サインアップ
from django.forms import EmailField
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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
        fields = ('author', 'text',)


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