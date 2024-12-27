import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Category, Tag


# Create your views here.

@csrf_exempt
def api(request):
    if request.method == 'GET':
        posts = Post.objects.all()
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
             'updatedAt': post.updated_at,
             },
            status=201)
