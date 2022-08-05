import json

from django.contrib.auth import get_user_model

from pages.models import Page, Like
from pages.serializers.page_serializers import StatsPageSerializer


User = get_user_model()


def get_stats(user: User):
    pages = Page.objects.filter(owner_id=user.id)

    data = dict(
        id=user.id,
        username=user.username,
        page_amount=pages.count(),
        likes_amount=Like.objects.filter(owner_id=user.id).count(),
        pages=StatsPageSerializer(instance=pages, many=True).data
    )
    return json.dumps(data)
