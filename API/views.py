import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse({'error': 'Please provide both username and email and password'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        try:
            user = User.objects.create_user(username=username, email=email, password=make_password(password))
        except IntegrityError:
            return JsonResponse({'error': 'Server Error'}, status=400)

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


class HomeView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({
            'message': f'Hello {user.username}',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)
