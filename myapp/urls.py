from django.urls import path
from . import views



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
    path("vietnam_research/post_okini/<int:user_id>/<int:program_id>",views.post_okini,name="post_okini"),
    path("vietnam_research/like_com/<int:user_id>/<int:comment_id>",views.like_com,name="like_com"),
    path('program/search/', views.post_search, name='post_search'),
    path('program/search/genre', views.genre_search, name='genre_search'),
    path('program/search/dj', views.dj_search, name='dj_search'),
]