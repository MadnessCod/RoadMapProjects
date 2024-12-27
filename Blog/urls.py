from django.urls import path
from .views import api

urlpatterns = [
    path('posts/', api, name='posts'),
    path('posts/<int:post_id>/', api, name='post detail'),
]
