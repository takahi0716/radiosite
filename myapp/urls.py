from django.urls import path
from . import views



urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('program/<int:pk>/', views.post_detail, name='post_detail'),
    path('program/new/', views.post_new, name='post_new'),
    path('program/<int:pk>/edit/', views.post_edit, name='post_edit'),
]