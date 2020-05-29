"""radiosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('myapp/', include('myapp.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views
# ログイン・サインアップ
from myapp import views as viewss

from myapp.views import Top

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # 1. 元々提供されている機能へ振り分け
    path('', include('myapp.urls')),
    # ログイン・サインアップ
    path('create_account', viewss.SignUpView.as_view(), name='create_account') ,
    path('accounts/', include('myapp.urls')), # 2. 自作の機能へ振り分け
]
