from rest_framework import serializers
from .models import User, Book

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']


class BookSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Keeps it read-only when fetching
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="author", write_only=True
    )  # Allows setting the author while creating/updating

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'publication_date', 'edition', 'price']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)  # Enforce a min length for security

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
