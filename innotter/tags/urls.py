from django.urls import path
from .views import tags_view

urlpatterns = [
    path('tags/', tags_view)
]
