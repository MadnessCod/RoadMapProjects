from django.urls import path

from .views import register, login, add_todo, update_todo, delete

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('todos/', add_todo, name='add'),
    path('todos/<int:todo_id>', update_todo, name='update'),
    path('delete/<int:todo_id>', delete, name='delete'),
]
