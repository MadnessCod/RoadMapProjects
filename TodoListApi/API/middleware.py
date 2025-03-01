import time

from django.http import JsonResponse
from django.core.cache import cache


class Costume404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return JsonResponse({'error': 'Not Found'}, status=404)
        if response.status_code == 500:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
        return response


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        limit = 60
        window = 120

        user_key = self.get_user_key(request)

        request_data = cache.get(user_key, (0, time.time()))
        request_count, first_request_time = request_data

        current_time = time.time()
        if current_time - first_request_time > window:
            request_data = (1, current_time)
        else:
            if request_count >= limit:
                retry_after = int(window - (current_time - first_request_time))
                return JsonResponse({'error': 'Too many requests',
                                     'retry_after': retry_after},
                                    status=429)
            else:
                request_data = (request_count + 1, first_request_time)

        cache.set(user_key, request_data, timeout=window)

        return self.get_response(request)

    def get_user_key(self, request):
        if request.user.is_authenticated:
            return f'user_{request.user.id}'
        return f'ip_{self.get_client_ip(request)}'

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
