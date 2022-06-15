from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view

from innotter.views import SerializersPermissionsViewSet
from . import serializers
from .models import Page


@api_view()
def pages_view(request):
    return Response({"message": "Pages"})


class PagesViewSet(SerializersPermissionsViewSet):

    queryset = Page.objects.all()
    default_serializer_class = serializers.PageSerializer

    serializer_classes_by_action = {
        'create': serializers.PageSerializer,
        'update': serializers.PageSerializer,
        'list': serializers.PageSerializer,
        'retrieve': serializers.PageSerializer,
    }

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }
