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
        fields = ('id', 'post', 'owner',)
        read_only_fields = ('owner',)


class UpdateLikeSerializer(BaseLikeSerializer):
    class Meta(BaseLikeSerializer.Meta):
        fields = ('post',)


class RetrieveLikeSerializer(BaseLikeSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta(BaseLikeSerializer.Meta):
        fields = ('id', 'post', 'owner')
