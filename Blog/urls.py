from django.urls import path

from Blog import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('<int:article_di>/', views.article, name='article'),
    path('admin/', views.admin, name='admin'),
    path('<int:article_id>/', views.add, name='add'),
    path('new/', views.new, name='new'),
]
