from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from Blog import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('articles/', views.home, name='articles'),
    path('<int:article_di>/', views.article, name='article'),
    path('dashboard/', views.admin, name='admin'),
    path('add_article/', views.add, name='add_article'),
    path('new/', views.new, name='new'),
]
