from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Expense


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already registered')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ExpenseSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'name', 'description', 'amount', 'category', 'category_display', 'user']
        read_only_fields = ['id', 'user', 'category_display']

    def validate_category(self, category):
        valid_categories = [i for tup in Expense.CATEGORY_CHOICES for i in tup]

        if category not in valid_categories:
            raise serializers.ValidationError(
                f'Valid Categories are {", ".join(valid_categories)}'
            )
        return category
