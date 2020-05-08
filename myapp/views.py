from django.shortcuts import render
from .models import Program
from django.utils import timezone

def post_list(request):
    programs = Program.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myapp/post_list.html', {'programs': programs})
