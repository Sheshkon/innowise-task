from rest_framework import serializers
from pages.models import Like


class BaseLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like


class LikeSerializer(BaseLikeSerializer):
    class Meta(BaseLikeSerializer.Meta):
        fields = '__all__'


class CreateLikeSerializer(BaseLikeSerializer):
    class Meta(BaseLikeSerializer.Meta):
        fields = '__all__'


class UpdateLikeSerializer(BaseLikeSerializer):
    class Meta(BaseLikeSerializer.Meta):
        fields = '__all__'


class RetrieveLikeSerializer(BaseLikeSerializer):

    class Meta(BaseLikeSerializer.Meta):
        fields = '__all__'
