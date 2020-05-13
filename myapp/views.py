from django.shortcuts import render, HttpResponse
from .models import *
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, StationForm, StationFormset, DjFormset, ListenerFormset
# post_detail ページを表示できれば良いですよね?
# そのために次のインポートを追加

from django.shortcuts import redirect
# roginuser only
from django.contrib.auth.decorators import login_required


def post_list(request):
    programs = Program.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myapp/post_list.html', {'programs': programs})


def post_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    return render(request, 'myapp/post_detail.html', {'program': program})

@login_required
def post_draft_list(request):
    programs = Program.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'myapp/post_draft_list.html', {'programs': programs})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Program, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Program, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Program, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.program = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'myapp/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.program.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.program.pk)


@login_required
def post_new(request):
    form = PostForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        station_formset = StationFormset(request.POST, instance=post)
        if station_formset.is_valid():
            post.save()
            station_formset.save()
            # return redirect('app:index')
            return redirect('post_detail', pk=post.pk)
        # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納
        else:
            context['station_formset'] = station_formset


        dj_formset = DjFormset(request.POST, instance=post)
        if dj_formset.is_valid():
            post.save()
            dj_formset.save()
            return redirect('post_detail', pk=post.pk)
        # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納
        else:
            context['dj_formset'] = dj_formset

        listener_formset = ListenerFormset(request.POST, instance=post)
        if listener_formset.is_valid():
            post.save()
            listener_formset.save()
            return redirect('post_detail', pk=post.pk)
        # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納
        else:
            context['listener_formset'] = listener_formset

    # GETのとき
    else:
        # 空のformsetをテンプレートへ渡す
        context['station_formset'] = StationFormset()
        context['dj_formset'] = DjFormset()
        context['listener_formset'] = ListenerFormset()

    return render(request, 'myapp/post_edit.html', context)

from django import forms 
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Program, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    station_formset = StationFormset(request.POST or None, instance=post)
    dj_formset = DjFormset(request.POST or None, instance=post)
    listener_formset = ListenerFormset(request.POST or None, instance=post)

    if request.method == 'POST' and form.is_valid() and station_formset.is_valid() and dj_formset.is_valid() and listener_formset.is_valid():
        form.save()
        station_formset.save()
        dj_formset.save()
        listener_formset.save()
        # 詳細ページを表示
        return redirect('post_detail', pk=pk)

    context = {
        'form': form,
        'station_formset': station_formset,
        'dj_formset': dj_formset,
        'listener_formset': listener_formset,
    }
    # 編集ページを再度表示
    return render(request, 'myapp/post_edit.html', context)

# @login_required
# def post_okini(request, user_id, program_id):
#     """いいねボタンをクリック"""
#     if request.method == 'POST':
#         query = Okini.objects.filter(user_id=user_id, program_id=program_id)
#         if query.count() == 0:
#             okini_tbl = Okini()
#             okini_tbl.user_id = user_id
#             okini_tbl.articles_id = program_id
#             okini_tbl.save()
#         else:
#             query.delete()

        # necessary return?
        # return HttpResponse("ajax is done!")





# def post_okini(request, *args, **kwargs):
#     program = get_object_or_404(Program, id=kwargs['program_id'])
#     is_okini = Okini.objects.filter(user=request.user).filter(program=program).count()

#     # unlike
#     if is_okini > 0:
#         liking = Okini.objects.get(program__id=kwargs['program_id'], user=request.user)
#         liking.delete()
#         program.okini_num -= 1
#         program.save()
#         return redirect('myapp/post_edit.html', kwargs={'post_id': kwargs['post_id']})
#     else:
#         # like
#         program.okini_num += 1
#         program.save()
#         okini = Okini()
#         okini.user = request.user
#         okini.post = program
#         okini.save()

#         return redirect('myapp/post_edit.html', kwargs={'post_id': kwargs['post_id']})

