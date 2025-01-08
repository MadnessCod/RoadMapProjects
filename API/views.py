from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email, MaxLengthValidator
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import User, TodoList, Category
from .utils import json_validator, authenticate_user, validate_todo, validate_date


# Create your views here.


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data, error = json_validator(request.body)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        if not data.get('name') or not data.get('email') or not data.get('password'):
            return JsonResponse({'error': 'Missing required field'}, status=401)

        try:
            validate_email(data.get('email'))
        except ValidationError:
            return JsonResponse({'error': 'Invalid email'}, status=400)

        try:
            user = User.objects.create(
                name=data.get('name'),
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
        data, error = json_validator(request.body)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        if not data.get('email') or not data.get('password'):
            return JsonResponse({'error': 'credential missing'}, status=401)

        try:
            user = User.objects.get(email=data.get('email'))
            if check_password(data.get('password'), user.password):
                return JsonResponse({'token': str(user.token)}, status=200)
            else:
                return JsonResponse({'error': 'invalid credential'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Email does not exist'}, status=401)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def add_todo(request):
    if request.method == 'POST':
        data, error = json_validator(request.body)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        user, error = authenticate_user(request)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        if not any(data.get(key) for key in ['title', 'description', 'category']):
            return JsonResponse({'message': 'Missing required field'}, status=401)

        try:
            max_length = MaxLengthValidator(20)
            max_length(data.get('category'))
            category = Category.objects.get_or_create(name=data.get('category'))[0]
        except ValidationError:
            return JsonResponse({'error': 'category length exceeds 20 characters'}, status=400)

        todo = TodoList.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            author=user,
            category=category,
        )

        return JsonResponse({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'category': todo.category.name,
        },
            status=201)

    if request.method == 'GET':
        user, error = authenticate_user(request)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        start_date = end_date = None

        if request.GET.get('start'):
            start_date, error = validate_date(request.GET.get('start'))
            if error:
                return JsonResponse({'error': error['error']}, status=error['status'])
        if request.GET.get('end'):
            end_date, error = validate_date(request.GET.get('end'))
            if error:
                return JsonResponse({'error': error['error']}, status=error['status'])

        try:
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 10))
            category = request.GET.get('category')
        except ValueError:
            return JsonResponse({'error': 'Invalid number for page or limit'}, status=400)

        todos = TodoList.objects.all()

        if start_date and end_date:
            todos = todos.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )
        elif start_date:
            todos = todos.filter(created_at__gte=start_date)
        elif end_date:
            todos = todos.filter(created_at__lte=end_date)

        if category:
            try:
                category = Category.objects.get(name=category)
                todos = todos.filter(category=category)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category does not exist'}, status=401)

        start = (page - 1) * limit
        end = start + limit

        todos = todos[start:end]

        if not todos and page != 1:
            start = 0
            end = limit
            todos = todos[start:end]
            page = 1

        todos_list = [
            {'id': todo.id,
             'title': todo.title,
             'description': todo.description,
             'category': todo.category.name,
             } for todo in todos
        ]
        return JsonResponse({
            'data': todos_list,
            'page': page,
            'limit': limit,
            'total': len(todos_list)},
            status=200)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def update_todo(request, todo_id):
    if request.method == 'PUT':
        user, error = authenticate_user(request)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        data, error = json_validator(request.body)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        if not any(data.get(key) for key in ['title', 'description', 'category']):
            return JsonResponse({'message': 'Missing required field'}, status=401)

        todo, error = validate_todo(todo_id, user)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        if data.get('title'):
            todo.title = data.get('title')
        if data.get('description'):
            todo.description = data.get('description')
        if data.get('category'):
            todo.category = Category.objects.get_or_create(name=data.get('category'))[0]

        todo.save()
        return JsonResponse({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'category': todo.category.name,
        },
            status=201)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def delete(request, todo_id):
    if request.method == 'DELETE':
        user, error = authenticate_user(request)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        todo, error = validate_todo(todo_id, user)
        if error:
            return JsonResponse({'error': error['error']}, status=error['status'])

        todo.delete()
        return JsonResponse({'message': 'deleted successfully'}, status=200)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
