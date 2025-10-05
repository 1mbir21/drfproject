from rest_framework import serializers
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone", "adress", "date_of_birth"]


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "profile",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
        ]

        def validate_email(self, value):
            """Проверка уникальности email"""
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    "A user with this email already exists."
                )
            return value

        def validate_username(self, value):
            """Проверка уникальности username"""
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError(
                    "A user with this username already exists."
                )
            return value

        def validate_password(self, value):
            try:
                validate_password(value)
            except ValidationError as e:
                raise serializers.ValidationError(e.message)
            return value

        def validate(self, attrs):
            if attrs["password"] != attrs["password_confirm"]:
                raise serializers.ValidationError("Passwords do not match.")
            return attrs

        def create(self, validated_data):
            validated_data.pop("password_confirm", None)
            user = User.objects.create_user(**validated_data)
            UserProfile.objects.create(user=user)
            return user
