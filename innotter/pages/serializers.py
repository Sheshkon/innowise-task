from rest_framework import serializers
from .models import Page


class BasePageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page


class PageSerializer(BasePageSerializer):

    class Meta(BasePageSerializer.Meta):
        fields = '__all__'



