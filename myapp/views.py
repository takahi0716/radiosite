from django.shortcuts import render
from .models import Program
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

def post_list(request):
    programs = Program.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myapp/post_list.html', {'programs': programs})


def post_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    return render(request, 'myapp/post_detail.html', {'program': program})