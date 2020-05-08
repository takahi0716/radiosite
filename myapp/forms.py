from django import forms

from .models import Program

class PostForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ('title', 'corner_title',)