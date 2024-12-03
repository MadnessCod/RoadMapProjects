from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import CustomUserCreationForm


# Create your views here.

def home(request):
    return render(request, 'articles.html')


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
        articles = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'articles.html', {'articles': articles})


def admin(request):
    pass


def add(request):
    pass


def new(request, article_id):
    pass
