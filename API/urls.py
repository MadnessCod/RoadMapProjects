from django.urls import path

from .views import register, login, add_todo, update_todo

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('todos/', add_todo, name='add'),
    path('todos/<int:todo_id>', update_todo, name='update'),
]
