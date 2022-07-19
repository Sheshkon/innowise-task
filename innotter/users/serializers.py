from django.contrib.auth import get_user_model
from rest_framework import serializers

from innotter.aws_services import get_presigned_url

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation.get('image_s3_path'):
            return representation

        representation['image_s3_path'] = get_presigned_url(representation['image_s3_path'])

        return representation


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer):
        model = User
        fields = '__all__'


class CreateUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'title', 'image_s3_path')
        extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'is_active', 'role', 'is_blocked', 'username', 'image_s3_path')


class UpdateUserInfoSerializer(BaseUserSerializer):
    file = serializers.FileField(allow_null=True, write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'username', 'email', 'image_s3_path', 'file')


class RetrieveUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        exclude = ('password',)


class LoginSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        exclude = ('password',)


class RegistrationSerializer(BaseUserSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta(BaseUserSerializer.Meta):
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

