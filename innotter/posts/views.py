from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def posts_view(request):
    return Response({"message": "Posts"})
