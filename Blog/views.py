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
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        is_author = article.author == request.user
        print(is_author)
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'article.html', {'article': article, 'is_author': is_author})


@login_required()
def edit_article(request, article_id):
    article = Article.objects.get(pk=article_id)

    if article.author != request.user:
        return HttpResponse(f'You can\'t edit this article, because the author is {article.author} and the user is {request.user.id} and {article.author == request.user}')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {"form": form, 'article': article})


@login_required()
def delete_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404

    if article.author != request.user:
        return HttpResponse("You can\'t delete this article.")

    if request.method == 'POST':
        article.delete()
        return redirect('articles')  # Redirect to the blogs page after deletion
    return render(request, 'confirm_delete.html', {'article': article})


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
