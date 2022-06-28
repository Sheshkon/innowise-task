from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer):
        model = User
        fields = '__all__'


class CreateUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'title',)
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

