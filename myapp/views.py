from django.shortcuts import render, HttpResponse
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, StationForm, StationFormset, DjFormset, ListenerFormset
# post_detail ページを表示できれば良いですよね?
# そのために次のインポートを追加

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
# 検索用
from django.contrib import messages
from functools import reduce
from operator import and_
from django.contrib.auth import login, authenticate
# ログイン・サインアップ

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)
from .forms import UserCreateForm

def post_list(request):
    # 時刻
    t_now = datetime.datetime.now().time()
    # 日付
    today = datetime.date.today()
    # ログイン中のユーザー
    # user = request.user.id

    # 0:月〜6:日であり、DBに合わせて１をたす
    youbi = today.weekday()+1

    programs = {}
    for i in Genre.objects.all():
        programs[i] = Program.objects.filter(genrelist__in=[i.id]).order_by('okini_num').reverse()[:5]

    # 開始時間＜＝現在時刻、終了時間＞現在時刻
    onair_programs_TBS = Station.objects.filter(station_name=1, day_of_the_week=youbi,start_time__lte=t_now, end_time__gt=t_now,)

    # コメント
    new_coments = Comment.objects.all().order_by('created_date').reverse()[:5]

    # 運営からのお知らせ
    infos = Info.objects.all().order_by('created_date').reverse()[:5]

    # ジャンル
    genres = Genre.objects.all()

    # パーソナリティ
    djs = Dj.objects.all().order_by('dj_name')


    context = {
        'programs': programs,
        'onair_programs_TBS': onair_programs_TBS,
        'new_coments':new_coments,
        'infos':infos,
        'genres':genres,
        'djs':djs,
    }
    return render(request, 'myapp/post_list.html', context)


def post_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    # ログイン中のユーザー
    user = request.user.id

    if user != '':
        okini_sign = Okini.objects.filter(user_id=user  , program_id=program.id).count()
        program.okini_num = program.okini_program.count()
        program.save()
        context = {
            'program': program,
            'okini_sign': okini_sign,
        }
    else:
        context = {
            'program': program,
        }
    return render(request, 'myapp/post_detail.html', context)

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

@login_required
def post_okini(request, user_id, program_id):
    """お気に入りボタンをクリック"""
    if request.method == 'POST':
        query = Okini.objects.filter(user_id=user_id, program_id=program_id)
        if query.count() == 0:
            okini_tbl = Okini()
            okini_tbl.user_id = user_id
            okini_tbl.program_id = program_id
            okini_tbl.save()
        else:
            query.delete()

        # necessary return?
        return HttpResponse("ajax is done!")
        # return redirect('post_list')

@login_required
def like_com(request, user_id, comment_id):
    """いいねボタンをクリック"""
    if request.method == 'POST':

        comment = get_object_or_404(Comment, pk=comment_id)
        like_num = Comment.objects.filter(pk=comment_id,like_user=user_id).count()
        if like_num > 0:
            comment.like_user.remove(user_id)
            comment.save()

        else:
            comment.like_user.add(user_id)
            comment.save()

        # necessary return?
        return HttpResponse("ajax is done!")

def post_search(request):
    program = Program.objects.order_by('-id')
    """ 検索機能の処理 """
    keyword = request.GET.get('keyword')
    if keyword:
        """ 除外リストを作成 """
        exclusion_list = set([' ', '　'])
        q_list = ''
        for i in keyword:
            """ 全角半角の空文字が含まれていたら無視 """
            if i in exclusion_list:
                pass
            else:
                q_list += i
        query = reduce(
            and_, [
                Q(title__icontains=q)
                | Q(corner_title__icontains=q)
                | Q(address__icontains=q)
                | Q(url__icontains=q)

                for q in q_list
            ]
        )
        program = program.filter(query)
        messages.success(request, '「{}」の検索結果'.format(keyword))

    context = {
        'program': program,
        'keyword': keyword,
    }
    return render(request, 'myapp/post_search.html', context)

# 絞り込み
def genre_search(request):
    # デフォルトは全件取得
    program = Program.objects.all().order_by('okini_num').reverse()

    # GETのURLクエリパラメータを取得する
    # 該当のクエリパラメータが存在しない場合は、[]が返ってくる
    q_genres = request.GET.getlist('genre')

    # ジャンルでの絞込は、genre.pkとして存在してる値のみ対象とする
    # "a"とかを指定するとValueErrorになるため
    check=[]
    for i in Genre.objects.all():
        check.append(str(i.id))


    keyword=''
    if len(q_genres) != 0:
        genres = [x for x in q_genres if x in check]
        # 重複を削除
        program = program.filter(genrelist__in=genres).distinct()
        for pk in genres:
            result = str(Genre.objects.get(pk__in=pk))
            keyword += result + ' '

    context = {
        'program': program,
    }
    messages.success(request, '「{}」の検索結果'.format(keyword))
    return render(request, 'myapp/post_search.html', context)


# 絞り込み
def dj_search(request):
    # デフォルトは全件取得
    program = Program.objects.all().order_by('okini_num').reverse()

    # GETのURLクエリパラメータを取得する
    # 該当のクエリパラメータが存在しない場合は、[]が返ってくる
    q_djs = request.GET.getlist('dj')

    # ジャンルでの絞込は、genre.pkとして存在してる値のみ対象とする
    # "a"とかを指定するとValueErrorになるため
    check=[]
    for i in Dj.objects.all():
        check.append(str(i.id))


    keyword=''
    if len(q_djs) != 0:
        djs = [x for x in q_djs if x in check]
        # 重複を削除
        djid = Dj.objects.filter(pk__in=djs).values('program')
        program = program.filter(pk__in=djid).distinct()
        for pk in djs:
            result = str(Dj.objects.get(pk__in=pk))
            keyword += result + ' '

    context = {
        'program': program,
    }
    messages.success(request, '「{}」の検索結果'.format(keyword))
    return render(request, 'myapp/post_search.html', context)




User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'myapp/post_list.html'


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        return render(self.request,'registration/profile.html')


class DeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user.email)
        user.is_active = False
        user.save()
        auth_logout(self.request)
        return render(self.request,'registration/delete_complete.html')


def user_detail(request, pk):
    user = get_object_or_404(Program, pk=pk)

    # ログイン中のユーザー
    login_user = request.user.id

    if user == login_user:

        context = {
            'user': user,
        }
    else:
        context = {
            'user': user,
        }
    return render(request, 'myapp/user_detail.html', context)