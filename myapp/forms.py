from django import forms

from .models import Program, Comment, Station

class PostForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ('title', 'corner_title',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class StationForm(forms.ModelForm):

    class Meta:
        model = Station
        fields = ('station_name',)