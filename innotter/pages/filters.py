from django_filters import rest_framework
from pages.models import Page


class PageFilter(rest_framework.FilterSet):

    tags = rest_framework.CharFilter(field_name='tags__name')

    class Meta:
        fields = ('uuid', 'name', 'tags')
        model = Page
