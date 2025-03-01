from django.http import JsonResponse


class Costume404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return JsonResponse({'error': 'Resource Not Found'}, status=404)
        if response.status_code == 500:
            return JsonResponse({'error': 'Internal Error'}, status=500)
        return response
