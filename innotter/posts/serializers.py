from rest_framework import serializers
from .models import Post


class BasePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post


class PostSerializer(BasePostSerializer):

    class Meta(BasePostSerializer.Meta):
        fields = '__all__'


class CreatePostSerializer(BasePostSerializer):

    class Meta(BasePostSerializer.Meta):
        exclude = ('created_at',  'updated_at')


class UpdatePostSerializer(BasePostSerializer):

    class Meta(BasePostSerializer.Meta):
        fields = ('id', 'content')


class RetrievePostSerializer(BasePostSerializer):
    page = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reply_to = serializers.SlugRelatedField(slug_field='content', read_only=True)

    class Meta(BasePostSerializer.Meta):
        fields = ('id', 'content', 'created_at',  'updated_at', 'page', 'reply_to')
