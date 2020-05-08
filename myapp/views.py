from django.shortcuts import render
from .models import Program
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
# post_detail ページを表示できれば良いですよね? そのために次のインポートを追加
from django.shortcuts import redirect

def post_list(request):
    programs = Program.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myapp/post_list.html', {'programs': programs})


def post_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    return render(request, 'myapp/post_detail.html', {'program': program})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myapp/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Program, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'myapp/post_edit.html', {'form': form})