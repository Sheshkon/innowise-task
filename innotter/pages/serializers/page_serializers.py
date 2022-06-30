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
        read_only_fields = ('unblock_date', )


class CreatePageSerializer(BasePageSerializer):
    class Meta(BasePageSerializer.Meta):
        fields = ('id', 'uuid', 'description', 'image', 'is_private')


class RetrievePageSerializer(BasePageSerializer):
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    followers = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)

    class Meta(BasePageSerializer.Meta):
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers', 'image',
                  'is_private', 'unblock_date', 'is_permanent_blocked')


class UpdatePageSerializer(BasePageSerializer):

    class Meta(BasePageSerializer.Meta):
        fields = ('name', 'uuid', 'description', 'image', 'is_private',)


class ListPageSerializer(BasePageSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta(BasePageSerializer.Meta):
        fields = ('id', 'name', 'owner', 'tags', 'is_private',)


class TagsToPageSerializer(BasePageSerializer):
    list_tag_names = serializers.ListSerializer(child=serializers.CharField(), required=False, write_only=True)

    class Meta(BasePageSerializer.Meta):
        fields = ('id', 'tags', 'list_tag_names',)
        read_only_fields = ('tags',)


class ListFollowRequestSerializer(BasePageSerializer):
    follow_requests = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)

    class Meta(BasePageSerializer.Meta):
        fields = ('id', 'name', 'owner', 'follow_requests')


class AcceptRequestSerializer(BasePageSerializer):
    one = serializers.BooleanField(default=False)
    user_id = serializers.CharField(required=False, write_only=True)

    class Meta(BasePageSerializer.Meta):
        fields = ('id', 'one', 'user_id')
