from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('register/', views.RegisterPageView.as_view(), name='register'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutPageView.as_view(), name='logout'),
    path('boards/user/<int:pk>/', views.UserPage.as_view(), name='user-page'),
    path('boards/', views.BoardsView.as_view(), name='boards'),
    path('boards/<slug:slug>/', views.PostsView.as_view(), name='posts'),
    path('boards/<slug:slug>/create/', views.PostCreateView.as_view(), name='posts-create'),
    path('boards/<slug:slug>/post-<int:pk>/edit/', views.PostEditView.as_view(), name='post-edit'),
    path('boards/<slug:slug>/post-<int:pk>/', views.PostView.as_view(), name='post-details'),
]