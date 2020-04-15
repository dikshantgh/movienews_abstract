# core/urls.py
"""This is the url route for core app"""
from django.urls import path, include
from django.views.generic import TemplateView
import django.contrib.auth
from core import views

app_name = 'core'
urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/<uuid:id>/', views.ProfileShowView.as_view(), name='profile_show'),
    path('profile/update/<uuid:id>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('post/detail/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create-new/', views.PostCreateView.as_view(), name='post_create'),
]



