from rest_framework import serializers

from innotter.aws_services import get_presigned_url
from pages.models import Page
from pages.serializers.post_serializers import StatsPostSerializer


class BasePageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Page

    def get_image(self, obj):
        return get_presigned_url(obj.image)


class PageSerializer(BasePageSerializer):
    class Meta(BasePageSerializer.Meta):
        fields = '__all__'


class BlockPageSerializer(BasePageSerializer):
    is_to_permanent = serializers.BooleanField(write_only=True, default=False)

    class Meta(BasePageSerializer.Meta):
        fields = ('is_to_permanent', 'unblock_date')
        read_only_fields = ('unblock_date',)


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
    file = serializers.FileField(allow_null=True, write_only=True)

    class Meta(BasePageSerializer.Meta):
        fields = ('name', 'uuid', 'description', 'image', 'is_private', 'file')


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


class AcceptOrRejectRequestSerializer(BasePageSerializer):
    one = serializers.BooleanField(default=False)
    user_id = serializers.CharField(required=False, write_only=True)

    class Meta(BasePageSerializer.Meta):
        fields = ('id', 'one', 'user_id')


class StatsPageSerializer(BasePageSerializer):
    followers = serializers.SerializerMethodField()
    follow_requests = serializers.SerializerMethodField()
    posts = StatsPostSerializer(many=True)
    posts_amount = serializers.SerializerMethodField()

    class Meta(BasePageSerializer.Meta):
        fields = ('id', 'name', 'followers', 'follow_requests', 'posts_amount', 'posts')

    def get_followers(self, obj):
        return obj.followers.count()

    def get_follow_requests(self, obj):
        return obj.follow_requests.count()

    def get_posts_amount(self, obj):
        return obj.posts.count()

