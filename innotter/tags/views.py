from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins, viewsets
from .models import Tag
from .serializers import TagSerializer


@api_view()
def tags_view(request):
    return Response({"message": "Tags"})


class TagsViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
