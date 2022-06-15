from rest_framework import serializers
from .models import User


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer):
        model = User
        fields = '__all__'


class CreateUserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'title', )
        extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'is_active', 'role', 'is_blocked')


class UpdateUserInfoSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'username', 'email', 'image_s3_path')


class RetrieveUserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        exclude = ('password',)


class LoginSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ('username', 'password')
