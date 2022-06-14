from django.urls import path
from .views import users_view

urlpatterns = [
    path('users/', users_view)
]
