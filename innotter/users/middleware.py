from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from innotter.settings import JWT_WHITELIST
from .authentication import SafeJWTAuthentication


class AuthMiddleware(MiddlewareMixin):

    def __int__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if self.check_is_in_whitelist(request):
            return self.get_response(request)

        jwt_auth = SafeJWTAuthentication().authenticate(request)
        request.user = jwt_auth[0]
        return self.get_response(request)

    @staticmethod
    def check_is_in_whitelist(request):
        resolved_path = resolve(request.path)

        if resolved_path.url_name in JWT_WHITELIST and request.method == 'POST' or resolved_path.app_name == 'admin':
            return True

        return False
