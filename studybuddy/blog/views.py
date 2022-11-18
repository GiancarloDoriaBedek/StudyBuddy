from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView, FormView, FormMixin, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model

from .models import Board, Post, Comment
from .forms import CreateCommentForm, EditPostForm, CreatePostForm, LoginForm, RegisterForm

# Create your views here.
    
def homepage(request):
    if request.user.is_authenticated:
        return redirect('boards')
    return redirect('login')


class BoardsView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Board

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()

        return context


class PostsView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(board__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['board'] = Board.objects.get(slug=self.kwargs['slug'])

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.board = Board.objects.get(slug=self.kwargs['slug'])
        form.instance.owner = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts', kwargs={'slug': self.kwargs['slug']})


class PostEditView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Post
    form_class = EditPostForm
    template_name = 'blog/post_edit_form.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['board'] = Post.objects.get(pk=self.kwargs['pk']).board
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context

    
    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'slug': self.kwargs['slug'], 'pk': self.kwargs['pk']})


class PostView(LoginRequiredMixin, FormMixin, ListView):
    login_url = 'login'
    model = Post
    template_name = 'blog/post_details.html'
    form_class = CreateCommentForm

    def get_queryset(self):
        print(self.kwargs['pk'])
        return Comment.objects.filter(post__id=self.kwargs['pk'])

    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['board'] = Post.objects.get(pk=self.kwargs['pk']).board
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        context['form'] = CreateCommentForm()

        return context


    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'slug': self.kwargs['slug'], 'pk': self.kwargs['pk']})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)       
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])

        form.save()
        return super(PostView, self).form_valid(form)


class RegisterPageView(FormView):
    template_name = 'blog/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('boards')


    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)

        return super(RegisterPageView, self).form_valid(form)

    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('boards')

        return super(RegisterPageView, self).get(*args, **kwargs)


class LoginPageView(LoginView):
    template_name = 'blog/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True


    def get_success_url(self):
        return reverse_lazy('boards')


class LogoutPageView(LoginRequiredMixin, LogoutView):
    def get_success_url(self):
        return reverse_lazy('register')


class UserPage(LoginRequiredMixin, DetailView):
    template_name = 'blog/user.html'
    model = get_user_model()