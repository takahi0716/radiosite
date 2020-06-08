from django.urls import path
from . import views

from django.views.generic import TemplateView
from .views import ContactFormView, ContactResultView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('program/<int:pk>/', views.post_detail, name='post_detail'),
    path('program/new/', views.post_new, name='post_new'),
    path('program/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('program/<pk>/publish/', views.post_publish, name='post_publish'),
    path('program/<pk>/remove/', views.post_remove, name='post_remove'),
    path('program/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('comment/list/', views.comment_list, name='comment_list'),
    path("vietnam_research/post_okini/<int:user_id>/<int:program_id>",views.post_okini,name="post_okini"),
    path("vietnam_research/like_com/<int:user_id>/<int:comment_id>",views.like_com,name="like_com"),
    path('program/search/', views.post_search, name='post_search'),
    path('program/search/genre', views.genre_search, name='genre_search'),
    path('program/search/dj', views.dj_search, name='dj_search'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('delete_confirm', TemplateView.as_view(template_name='registration/delete_confirm.html'), name='delete-confirmation'),
    path('delete_complete', views.DeleteView.as_view(), name='delete-complete'),
    # 運営からのお知らせ
    path('info/', views.info_list, name='info_list'),
    # ユーザーページ
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('user/<int:pk>/edit/', views.user_edit, name='user_edit'),

    # お問い合わせ
    path('contact/', ContactFormView.as_view(), name='contact_form'),
    path('contact/result/', ContactResultView.as_view(), name='contact_result'),

    # 意見箱
    path('opinion/', views.opinion_form, name='opinion_form'),

    # ページ情報
    path('pageinfo/', views.pageinfo, name='pageinfo'),

    # 利用規約
    path('terms/', views.terms, name='terms'),

    # プライバシーポリシー
    path('privacy/', views.privacy, name='privacy'),
]