from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterView, ExpenseView, ExpenseUpdate, ExpenseDelete


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('expenses/', ExpenseView.as_view(), name='expenses'),
    path('expenses/<int:pk>/update/', ExpenseUpdate.as_view(), name='expense-update'),
    path('expenses/<int:pk>/delete/', ExpenseDelete.as_view(), name='expense_delete'),
]
