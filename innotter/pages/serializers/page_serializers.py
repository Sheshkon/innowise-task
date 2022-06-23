from rest_framework import serializers
from pages.models import Page


class BasePageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page


class PageSerializer(BasePageSerializer):

    class Meta(BasePageSerializer.Meta):
        fields = '__all__'


class BlockPageSerializer(BasePageSerializer):

    is_to_permanent = serializers.BooleanField(write_only=True, default=False)

    class Meta(BasePageSerializer.Meta):

        fields = ('is_to_permanent', 'unblock_date')
        extra_kwargs = {
            'unblock_date': {'read_only': True},
        }
