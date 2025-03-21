from django.utils.timezone import now, timedelta

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListCreateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Expense
from .serializers import UserRegisterSerializer, ExpenseSerializer


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpenseView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication,]
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        date_filter = request.query_params.get('date_filter', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        queryset = Expense.objects.filter(user=request.user)

        if date_filter == 'last_week':
            queryset = queryset.filter(created_at__gt=now() - timedelta(days=7))
        elif date_filter == 'last_month':
            queryset = queryset.filter(created_at__gt=now() - timedelta(days=30))
        elif date_filter == 'last_three_month':
            queryset = queryset.filter(created_at__gte=now() - timedelta(days=90))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if start_date and end_date:
            queryset = queryset.filter(created_at__gte=start_date, created_at_lte=end_date)

        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpenseUpdate(RetrieveUpdateAPIView):
    queryset = Expense.objects.all()
    authentication_classes = [JWTAuthentication,]
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ExpenseDelete(DestroyAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
