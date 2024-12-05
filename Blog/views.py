from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import CustomUserCreationForm, ArticleForm


# Create your views here.

def home(request):
    try:
        articles = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404('Webpage does not exist')

    return render(request, 'articles.html', {'articles': articles})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def article(request, article_id):
    try:
        article_content = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'articles.html', {'article': article_content})


def admin(request):
    pass


@login_required()
def add(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('articles')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})


def new(request, article_id):
    pass
