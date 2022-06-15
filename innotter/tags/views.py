from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view

from innotter.views import SerializersPermissionsViewSet
from . import serializers
from .models import Tag


@api_view()
def tags_view(request):
    return Response({"message": "Tags"})


class TagsViewSet(SerializersPermissionsViewSet):

    queryset = Tag.objects.all()
    default_serializer_class = serializers.TagSerializer

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }

