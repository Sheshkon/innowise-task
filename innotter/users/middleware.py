from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def __int__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

