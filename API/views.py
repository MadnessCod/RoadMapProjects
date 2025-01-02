import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import User, TodoList


# Create your views here.


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'massage not valid'}, status=400)

        if not data.get('name') or not data.get('email') or not data.get('password'):
            return JsonResponse({'error': 'Missing required field'}, status=401)

        try:
            validate_email(data.get('email'))
        except ValidationError:
            return JsonResponse({'error': 'Invalid email'}, status=400)

        try:
            user = User.objects.create(name=data.get('name'),
                                       email=data.get('email'),
                                       password=make_password(data.get('password'))
                                       )
        except IntegrityError as e:
            if 'email' in str(e).lower():
                return JsonResponse({'error': 'email already exists'}, status=400)
            return JsonResponse({'error': 'Database Error'}, status=500)

        return JsonResponse({'token': str(user.token)}, status=201)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'massage not valid'}, status=400)

        if not data.get('email') or not data.get('password'):
            return JsonResponse({'error': 'credential missing'}, status=401)

        try:
            user = User.objects.get(email=data.get('email'))
            if check_password(data.get('password'), user.password):
                return JsonResponse({'token': str(user.token)}, status=200)
            else:
                return JsonResponse({'error': 'invalid credential'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'invalid credential'}, status=401)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def add_todo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'massage not valid'}, status=400)

        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'message': 'Unauthorized'}, status=401)
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return JsonResponse({'error': 'invalid token'}, status=401)

        if not data.get('title') or not data.get('description'):
            return JsonResponse({'message': 'Missing required field'}, status=401)

        todo = TodoList.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            author=user
        )

        return JsonResponse({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
        },
            status=201)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def update_todo(request, todo_id):
    if request.method == 'PUT':
        if not request.headers.get('Authorization'):
            return JsonResponse({'message': 'Unauthorized'}, status=401)

        try:
            user = User.objects.get(token=request.headers.get('Authorization'))
        except User.DoesNotExist:
            return JsonResponse({'error': 'invalid token'}, status=401)

        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'massage not valid'}, status=400)

        if not data.get('title') or not data.get('description'):
            return JsonResponse({'message': 'Missing required field'}, status=401)

        try:
            todo = TodoList.objects.get(id=todo_id)
        except TodoList.DoesNotExist:
            return JsonResponse({'error': 'invalid id'}, status=401)

        if data.get('title'):
            todo.title = data.get('title')
        if data.get('description'):
            todo.description = data.get('description')

        todo.save()
        return JsonResponse({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
        },
            status=201)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
