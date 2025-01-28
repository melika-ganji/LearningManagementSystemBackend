from rest_framework import serializers
from accounts.models import CustomUser
from courses.models import Course, Category

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CourseSearchSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'category', 'price', 'is_public']

class CategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
