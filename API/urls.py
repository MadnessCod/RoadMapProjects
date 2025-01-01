from django.urls import path

from .views import register, login, add_todo

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('add/', add_todo, name='add'),
]
