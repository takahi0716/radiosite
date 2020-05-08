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
]