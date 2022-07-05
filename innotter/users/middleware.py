from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden

from innotter.settings import JWT_WHITELIST
from users.authentication import SafeJWTAuthentication


class AuthMiddleware(MiddlewareMixin):

    def __int__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if self.check_is_in_whitelist(request):
            return self.get_response(request)

        try:
            jwt_auth = SafeJWTAuthentication().authenticate(request)
            request.user = jwt_auth[0]
        except Exception as e:
            return HttpResponseForbidden(e)

        return self.get_response(request)

    @staticmethod
    def check_is_in_whitelist(request):
        resolved_path = resolve(request.path)

        if resolved_path.url_name in JWT_WHITELIST and request.method == 'POST' or resolved_path.app_name == 'admin':
            return True

        return False
