import json

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from .models import Post, Category, Tag


# Create your views here.

@ensure_csrf_cookie
def api(request, post_id=None):
    """
    Documentation for `api` Function in Django Blog App

    The `api` function is a view that serves as a RESTful endpoint for handling blog posts. It supports CRUD operations (Create, Read, Update, Delete) and allows users to search for posts.

    Parameters:
        request: HttpRequest object representing the incoming HTTP request.
        post_id: int or None, optional. If provided, specifies the ID of the post to operate on.

    Methods:

    1. GET:
        - Retrieves all posts or a specific post based on `post_id`.
        - Supports searching posts by title, content, or category using the `term` query parameter.
        - Response (for a specific post):
            ```json
            {
                "id": int,
                "title": str,
                "content": str,
                "category": str,
                "tags": [str],
                "createdAt": datetime,
                "updatedAt": datetime
            }
            ```
        - Response (for multiple posts):
            ```json
            [
                {
                    "id": int,
                    "title": str,
                    "content": str,
                    "category": str,
                    "tags": [str],
                    "createdAt": datetime,
                    "updatedAt": datetime
                },
                ...
            ]
            ```

    2. POST:
        - Creates a new post with the given data.
        - Requires JSON payload:
            ```json
            {
                "title": str,
                "content": str,
                "category": str,
                "tags": [str] or str
            }
            ```
        - Automatically creates new categories and tags if they don't already exist.
        - Response:
            ```json
            {
                "id": int,
                "title": str,
                "content": str,
                "category": str,
                "tags": [str],
                "createdAt": datetime,
                "updatedAt": datetime
            }
            ```

    3. PUT:
        - Updates an existing post identified by `post_id`.
        - Accepts partial updates to any combination of `title`, `content`, `category`, or `tags`.
        - Requires JSON payload with the fields to update:
            ```json
            {
                "title": str, // optional
                "content": str, // optional
                "category": str, // optional
                "tags": [str] // optional
            }
            ```
        - Response:
            ```json
            {
                "id": int,
                "title": str,
                "content": str,
                "category": str,
                "tags": [str],
                "createdAt": datetime,
                "updatedAt": datetime
            }
            ```

    4. DELETE:
        - Deletes an existing post identified by `post_id`.
        - Response:
            ```json
            {
                "message": "Post deleted"
            }
            ```

    Error Handling:
        - Returns `404 Not Found` if a specified post does not exist.
        - Returns `400 Bad Request` for invalid JSON payloads.
        - Returns `405 Method Not Allowed` for unsupported HTTP methods.

    Middleware:
        - Uses `@ensure_csrf_cookie` for CSRF protection in development.
    """
    if request.method == 'GET':
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return JsonResponse({'error': 'post not found'}, status=404)
            return JsonResponse({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'category': post.category.name,
                'tag': [tag.name for tag in post.tags.all()],
                'createdAt': post.created_at,
                'updatedAt': post.updated_at,
            }, safe=False, status=200)

        term = request.GET.get('term')
        posts = Post.objects.all()
        if term:
            posts = Post.objects.filter(Q(title__icontains=term) |
                                        Q(content__icontains=term) |
                                        Q(category__name__icontains=term))

        response_data = [
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'category': post.category.name,
                'tags': [tag.name for tag in post.tags.all()],
                'createAt': post.created_at,
                'updateAt': post.updated_at,
            }
            for post in posts
        ]
        return JsonResponse(response_data, safe=False, status=200)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        if not data.get('title') or not data.get('content') or not data.get('category') or not data.get('tags'):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        tags = data.get('tags')

        category, _ = Category.objects.get_or_create(name=data.get('category'))

        post = Post.objects.create(title=data['title'], content=data['content'], category=category)

        if isinstance(tags, list):
            for tag in tags:
                name, _ = Tag.objects.get_or_create(name=tag)
                post.tags.add(name)
        elif isinstance(tags, str):
            name, _ = Tag.objects.get_or_create(name=tags)
            post.tags.add(name)

        post.save()
        return JsonResponse(
            {'id': post.id,
             'title': post.title,
             'content': post.content,
             'category': post.category.name,
             'tags': [tag.name for tag in post.tags.all()],
             'createdAt': post.created_at,
             'updatedAt': post.updated_at,
             },
            status=201)

    elif request.method == 'PUT' and post_id:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post does not exist'}, status=404)

        if not any(data.get(key) for key in ('title', 'content', 'category', 'tags')):
            return JsonResponse({'error': 'at least one field must provided'}, status=400)

        if data.get('title'):
            post.title = data['title']

        if data.get('content'):
            post.content = data['content']

        if data.get('category'):
            post.category, _ = Category.objects.get_or_create(name=data['category'])

        if data.get('tags'):
            post.tags.clear()
            tags = data['tags']
            for tag in tags:
                name, _ = Tag.objects.get_or_create(name=tag)
                post.tags.add(name)

        post.save()

        return JsonResponse(
            {'id': post.id,
             'title': post.title,
             'content': post.content,
             'category': post.category.name,
             'tags': [tag.name for tag in post.tags.all()],
             'createdAt': post.created_at,
             'updatedAt': post.updated_at, },
            status=200,
        )

    elif request.method == 'DELETE' and post_id:
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post does not exist'}, status=404)

        post.delete()
        return JsonResponse({'message': 'Post deleted'}, status=204)

    return JsonResponse({'error': 'Method Not Allowed'}, status=405)
