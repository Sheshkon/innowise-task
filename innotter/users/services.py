from datetime import datetime, timedelta

import jwt
from rest_framework import exceptions

from .models import User
from innotter.settings import SECRET_KEY


def validate_user(data):
    username = data.get('username', None)
    password = data.get('password', None)

    if username is None:
        raise exceptions.AuthenticationFailed('Username required.')

    if password is None:
        raise exceptions.AuthenticationFailed('Password required.')

    user = User.objects.filter(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found.')
    if not user.is_active:
        raise exceptions.AuthenticationFailed('This user has been deactivated.')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Wrong password.')

    return user


def _create_jwt_token(user, days=0, minutes=0):

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=days, minutes=minutes),
        'iat': datetime.utcnow(),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token


def generate_access_token(user):
    return _create_jwt_token(user, minutes=5)


def generate_refresh_token(user):
    return _create_jwt_token(user, days=7)


def check_user_refresh_token(request):
    token = request.COOKIES.get('refreshtoken')
    if token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    return user


