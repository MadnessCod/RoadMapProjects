from django.utils.timezone import now, timedelta

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveUpdateAPIView

from .models import Expense
from .serializers import UserRegisterSerializer, ExpenseSerializer


# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data_filter = request.query_params.get('date_filter', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        queryset = Expense.objects.filter(user=request.user)

        if data_filter == 'last_week':
            queryset = queryset.filter(created_at__gt=now() - timedelta(days=7))
        elif data_filter == 'last_month':
            queryset = queryset.filter(created_at__gt=now() - timedelta(days=30))
        elif data_filter == 'last_three_month':
            queryset = queryset.filter(created_at__gte=now() - timedelta(days=90))

        if start_date and end_date:
            queryset = queryset.filter(created_at__gte=start_date, created_at_lte=end_date)

        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpenseUpdate(RetrieveUpdateAPIView):
    queryset = Expense.objects.all()
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

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
