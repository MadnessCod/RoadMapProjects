from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from Blog import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('articles/', views.home, name='articles'),
    path('<int:article_id>/', views.article, name='article'),
    path('dashboard/', views.admin, name='admin'),
    path('add_article/', views.add, name='add_article'),
    path('<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('<int:article_id>/delete/', views.delete_article, name='delete_article'),
    path('new/', views.new, name='new'),
]
