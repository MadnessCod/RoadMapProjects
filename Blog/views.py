import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Post, Category, Tag


# Create your views here.

@csrf_exempt
def api(request, post_id=None):
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

    elif request.method == 'PUT' and post_id:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post does not exist'}, status=404)

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
             'updatedAt': post.updated_at,},
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